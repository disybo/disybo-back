from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig
from database import db
from models.boy import Boy

app = Flask(__name__)
CORS(app)

app.config.from_object(DevelopmentConfig)


@app.route('/')
def blank():
    return 'Hello, world'


@app.route('/<int:user_id>')
def hello_world(user_id):
    try:
        name = Boy.query.get(user_id).name
        return "<h1>Hello, {}</ht>".format(name)
    except Exception as ex:
        print(ex)
        return '<h1>Something is broken.</h1>'


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
