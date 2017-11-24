from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Junction 2017! Can I get a hooray?! Daaaaaaaaang.\n'


if __name__ == '__main__':
    app.run()
