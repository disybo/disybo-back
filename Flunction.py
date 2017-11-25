from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import DevelopmentConfig
from database import db

from api.vehicle_station_data.models import Boy

# Import Blueprints
from api.vehicle_station_data.vehicles import vehicles
from api.vehicle_station_data.stations import stations

app = Flask(__name__)
CORS(app)

app.config.from_object(DevelopmentConfig)

migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(vehicles)
app.register_blueprint(stations)


@app.route('/')
def blank():
    return 'Hello, world'


@app.route('/tables')
def tables():
    from sqlalchemy import MetaData
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    tables = metadata.tables.keys()
    return " | ".join(tables)


@app.route('/users')
def all_users():
    users = db.session.query(Boy).all()
    return u"<br>".join([u"{0}: {1}".format(user.name, user.role) for user in users])


@app.route('/user/<int:user_id>')
def user(user_id):
    try:
        name = Boy.query.get(user_id).name
        return "<h1>Hello, {}</ht>".format(name)
    except Exception as ex:
        print(ex)
        return '<h1>Something is broken.</h1>'


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
