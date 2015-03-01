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

$('.home-pane .mix-bttn').click(function() { transitionPanes($('.mix-pane')) })

$('.home-pane .lucky-bttn').click(function() { transitionPanes($('.loading-pane')) })

$('.mix-pane .back-bttn').click(function() { transitionPanesRight($('.home-pane')) })

$('.mix-pane .mix-bttn').click(function() { transitionPanes($('.loading-pane')) })
