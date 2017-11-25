from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import DevelopmentConfig
from database import db

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


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
