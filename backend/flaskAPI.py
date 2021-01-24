from flask import Flask, jsonify

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
    text = FileParser(file)
    cat = ADAM_AND_RAZ_ML(text)
    return jsonify({"major": categories[0], "minor": categories[1]})


if __name__ == "__main__":
    app.run(debug=True)

