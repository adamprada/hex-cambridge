from flask import Flask, jsonify
import task_similarity.categorise as cat

app = Flask(__name__)


# @app.route("/file/<string:filename>/", methods=["GET"])
# def get_file_from_firebase(filename):
#     file = Firebase(filename)
#     return file


# @app.route("/parse_file", methods=["GET"])
# def parse_file(filename):
#     text = FileParser(filename)
#     return text


@app.route("/categories", methods=["GET"])
def categorise(file):
    # this is a list, [0] is major category, [1:] are top three minor matches
    category = cat(text)
    return jsonify({"major": categories[0], "minor": [categories[1:]]})


if __name__ == "__main__":
    app.run(debug=True)

