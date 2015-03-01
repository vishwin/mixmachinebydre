function transitionPanes(to) {
	var from = $('.panes > *:visible');
	var slideDistance = 300;
	var animationDuration = 200;
	// Move the next pane over to the right; we'll be sliding it in
	to.css({display: 'block', opacity: 0});
	toLeftOrig = to.css('left');
	to.css({left: parseInt(toLeftOrig, 10) + slideDistance + 'px'});
	// Fade out the current pane and move it over to the left
	from.animate({opacity: 0,
				  left: parseInt(from.css('left'), 10) - slideDistance + 'px'}, animationDuration,
				  function() { from.css({display: 'none', opacity: 1,
				  			   left: parseInt(from.css('left'), 10) + slideDistance + 'px'}) });
	// Fade in the next pane and move it over from the right
	to.animate({opacity: 1, left: toLeftOrig}, animationDuration);
}

function transitionPanesRight(to) {
	var from = $('.panes > *:visible');
	var slideDistance = 300;
	var animationDuration = 200;
	// Move the next pane over to the left; we'll be sliding it in
	to.css({display: 'block', opacity: 0});
	toLeftOrig = to.css('left');
	to.css({left: parseInt(toLeftOrig, 10) - slideDistance + 'px'});
	// Fade out the current pane and move it over to the right
	from.animate({opacity: 0,
				  left: parseInt(from.css('left'), 10) + slideDistance + 'px'}, animationDuration,
				  function() { from.css({display: 'none', opacity: 1,
							   left: parseInt(from.css('left'), 10) - slideDistance + 'px'}) });
	// Fade in the next pane and move it over from the right
	to.animate({opacity: 1, left: toLeftOrig}, animationDuration);
}

var numSelectedStars = 0;

function setStars(rating) {
	$('.stars .fa:nth-child(-n+' + rating + ')').removeClass('fa-star-o').addClass('fa-star');
	$('.stars .fa:nth-child(n+' + (rating + 1) + ')').removeClass('fa-star').addClass('fa-star-o');
	numSelectedStars = rating;
}

function mixValues(volume, values) {
	var queueWatchInterval;
	function watchJobQueue() {
		// Check to see if the mixing job has completed
		$.ajax({
			type: "GET",
			url: '/api/status'
		}).done(function(data) {
			if(data['message'] == 'Mixing 0 jobs') {
				window.clearInterval(queueWatchInterval);
				transitionPanes($('.rating-pane'))
				ratingScreen(values)
			}
		})
	}

	var params = {vol: volume};
	var url;
	if(values) {
		params['amnt1'] = values[0];
		params['amnt2'] = values[1];
		params['amnt3'] = values[2];
		params['amnt4'] = values[3];
		url = '/api/mix';
	}
	else {
		url = '/api/generate';
	}
	// Send AJAX request
	$.ajax({
		type: "POST",
		url: url,
		data: params
	}).done(function(data) {
		values = data['amounts'];
		transitionPanes($('.loading-pane'));
		// Check the job queue every second to see if it finished
		queueWatchInterval = window.setInterval(watchJobQueue, 1000);
	}).fail(function(jqXHR, textStatus) {
		console.log('AJAX mix request failed!!');
		console.log(jqXHR);
		console.log(textStatus);
		alert('An unexpected error occurred. Please check the console for details.');
	});
}

function ratingScreen(amounts) {
	$('.rating-pane .rect-bttn').click(function() {
		if(numSelectedStars == 0) {
			$('.mix-pane .error').text('Please provide a rating.');
			var totalHeight = $('.mix-pane').height() + $('.mix-pane .error').height() + 'px';
			$('.mix-pane').animate({height: totalHeight});
			$('.mix-pane .error').css({top: parseInt(totalHeight, 10) - $('.mix-pane .error').height() + 'px'}).delay(200).animate({opacity: 1});
		}
		else {
			$.ajax({
				type: "POST",
				url: '/api/rate',
				data: {amnt1: amounts[0], amnt2: amounts[1], amnt3: amounts[2], amnt4: amounts[3], rating: 2*numSelectedStars}
			}).done(function(data) {
				numSelectedStars = 0;
				$('.stars .fa-star').removeClass('fa-star').addClass('fa-star-o');
				transitionPanes($('.home-pane'));
			}).fail(function(jqXHR, textStatus) {
				console.log('AJAX mix request failed!!');
				console.log(jqXHR);
				console.log(textStatus);
				alert('An unexpected error occurred. Please check the console for details.');
			});
		}
	});
}

$('.home-pane .mix-bttn').click(function() { transitionPanes($('.mix-pane')) })

$('.home-pane .lucky-bttn').click(function() { transitionPanes($('.lucky-pane')) })

$('.mix-pane .back-bttn').click(function() { transitionPanesRight($('.home-pane')) })

//$('.mix-pane .mix-bttn').click(function() {transitionPanes($('.loading-pane')); setTimeout(function() {transitionPanes($('.rating-pane'))}, 1000) })
$('.mix-pane .mix-bttn').click(function() {
	function setError(msg) {
		$('.mix-pane .error').text(msg);
		if($('.mix-pane .error').css('opacity') != 1) {
			var totalHeight = $('.mix-pane').height() + $('.mix-pane .error').height() + 'px';
			$('.mix-pane').animate({height: totalHeight});
			$('.mix-pane .error').css({top: parseInt(totalHeight, 10) - $('.mix-pane .error').height() + 'px'}).delay(200).animate({opacity: 1});
		}
	}
	// Make sure we have some ingredients
	rangeSelector = $('.mix-pane .sliders input')
	if(rangeSelector[0].value == 0 && rangeSelector[1].value == 0 && rangeSelector[2].value == 0 && rangeSelector[3].value == 0) {
		setError('You need to select an ingredient first');
		return;
	}
	if(!$('.mix-pane .small-glass').is(':checked') && !$('.mix-pane .large-glass').is(':checked')) {
		setError('Please select a beverage size');
		return;
	}
	amounts = [rangeSelector[0].value, rangeSelector[1].value, rangeSelector[2].value, rangeSelector[3].value]
	volume = $('.mix-pane .small-glass').is(':checked') ? $('.mix-pane .small-glass').val() : $('.mix-pane .large-glass').val();
	mixValues(volume, amounts);
	// Reset the form
	$('.mix-pane .small-glass').prop('checked', false);
	$('.mix-pane .large-glass').prop('checked', false);
	$('.mix-pane .sliders > input').val(0);
})

$('.lucky-pane .back-bttn').click(function() { transitionPanesRight($('.home-pane')) })

//$('.lucky-pane .mix-bttn').click(function() { transitionPanes($('.loading-pane')); setTimeout(function() {transitionPanes($('.rating-pane'))}, 1000) })
$('.lucky-pane .mix-bttn').click(function() {
	function setError(msg) {
		$('.lucky-pane .error').text(msg);
		if($('.lucky-pane .error').css('opacity') != 1) {
			var totalHeight = $('.lucky-pane').height() + $('.lucky-pane .error').height() + 'px';
			$('.lucky-pane').animate({height: totalHeight});
			$('.lucky-pane .error').css({top: parseInt(totalHeight, 10) - $('.lucky-pane .error').height() + 'px'}).delay(200).animate({opacity: 1});
		}
	}
	if(!$('.lucky-pane .small-glass').is(':checked') && !$('.lucky-pane .large-glass').is(':checked')) {
		setError('Please select a beverage size');
		return;
	}
	volume = $('.mix-pane .small-glass').is(':checked') ? $('.mix-pane .small-glass').val() : $('.mix-pane .large-glass').val();
	mixValues(volume);
	// Reset the form
	$('.lucky-pane .small-glass').prop('checked', false)
	$('.lucky-pane .large-glass').prop('checked', false)
})
