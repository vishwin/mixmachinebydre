from webui import app, jobs
from flask import request, jsonify
from .ml import generate_suggestion, learn


class APIError(Exception):

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(APIError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({'message': 'Mixing {0} jobs'.format(len(jobs))})

@app.route('/api/mix', methods=['POST'])
def mix():
    if 'amnt1' not in request.form or \
       'amnt2' not in request.form or \
       'amnt3' not in request.form or \
       'amnt4' not in request.form or \
       'vol' not in request.form:
        raise APIError('All four amounts and the volume must be specified.')
    try:
        amounts = [float(request.form['amnt1']), float(request.form['amnt2']), float(request.form['amnt3']), float(request.form['amnt4'])]
        volume = float(request.form['vol'])   # in milliliters
    except ValueError:
        raise APIError('The amounts and volume specified must be floating point values.')
    # Convert the amounts from arbitrary numbers into a percentage
    amounts = [ x / sum(amounts) for x in amounts ]
    # Add the job to the queue
    jobs.append((volume, amounts))
    return jsonify({'message': 'Mixing...', 'amounts': amounts, 'volume': volume})

@app.route("/api/generate", methods=['POST'])
def generate():
    if 'vol' not in request.form:
        raise APIError('The volume must be specified.')
    try:
        volume = float(request.form['vol'])
    except ValueError:
        raise APIError('The volume specified must be a floating point value.')
    # Generate a suggestion
    amounts = generate_suggestion()
    jobs.append((volume, amounts))
    return jsonify({'message': 'Mixing...', 'amounts': amounts, 'volume': volume})

@app.route("/api/rate", methods=['POST'])
def rate():
    if 'amnt1' not in request.form or \
       'amnt2' not in request.form or \
       'amnt3' not in request.form or \
       'amnt4' not in request.form or \
       'rating' not in request.form:
        raise APIError('All four amounts and the rating must be specified.')
    try:
        amounts = [float(request.form['amnt1']), float(request.form['amnt2']), float(request.form['amnt3']), float(request.form['amnt4'])]
        rating = float(request.form['rating'])   # in milliliters
    except ValueError:
        raise APIError('The amounts and volume specified must be floating point values.')
    print("Learning...")
    learn(amounts, rating)
    return jsonify({'message': 'OK'})
