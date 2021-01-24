from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from text_similarity import categorise
import tempfile
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/machine_learning", methods=["POST"])
@cross_origin()
def machine_learning():
    f = request.files['file']
    f.save('/tmp/' + f.filename)
    # # this is a list, [0] is major category, [1:] are top three minor matches
    categories = categorise('/tmp/' + f.filename)
    return jsonify({"major": categories[0], "minor": [categories[1:]]})


if __name__ == "__main__":
    app.run(debug=True)

