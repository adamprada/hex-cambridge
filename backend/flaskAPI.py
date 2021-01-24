from flask import Flask, jsonify, request
from text_similarity import categorise
from werkzeug import secure_filename
from shutil import copyfile
import tempfile
import os

app = Flask(__name__)


# @app.route("/file/<string:filename>/", methods=["GET"])
# def get_file_from_firebase(filename):
#     file = Firebase(filename)
#     return file


# @app.route("/parse_file", methods=["GET"])
# def parse_file(filename):
#     text = FileParser(filename)
#     return text


@app.route("/machine_learning", methods=["GET"])
def machine_learning():
    f = request.files['file'].read()
    new_file, filename = tempfile.mkstemp()
    os.write(new_file, f)
    # # this is a list, [0] is major category, [1:] are top three minor matches
    categories = categorise(filename)
    os.close(new_file)
    return jsonify({"major": categories[0], "minor": [categories[1:]]})


if __name__ == "__main__":
    app.run(debug=True)

