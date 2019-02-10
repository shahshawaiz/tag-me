from flask import Flask, jsonify, request
import analyzer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def analyze():

    response = {
        "status": 200,
         "message": "Welcome to TagMe. Send me your images, get your labels ;) "
    }

    return jsonify(response), 200

@app.route('/', methods=['POST'])
def analyze():
    if not request.json or not 'url' in request.json:
        abort(400)

    url = request.json['url']

    labels = analyzer.predict_label(url)

    response = {
    	"status": 200,
    	"labels": labels
    }

    return jsonify(response), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)

if __name__ == '__main__':
    
    app.run(
        host=0.0.0.0,
        port=80,
        debug=False
    )   