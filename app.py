from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# My App
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    return "Testing 123"


if __name__ in "__main__":
    app.run(debug=True)