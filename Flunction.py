from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello Junction 2017! Can I get a hooray?! Daaaaaaaaang.\n'


if __name__ == '__main__':
    app.run(debug=True)
