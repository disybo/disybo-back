from flask import Blueprint
from .models import Boy, Vehicle, VehicleType, RefuelEvent, FuelStation, FuelType
from database import db

vehicles = Blueprint('vehicles', 'vehicles', url_prefix='/api/vehicles')


@vehicles.route('/boys/<int:user_id>')
def hello_world(user_id):
    try:
        name = Boy.query.get(user_id).name
        return "<h1>Hello, {}</ht>".format(name)
    except Exception as ex:
        print(ex)
        return '<h1>Something is broken.</h1>'


@vehicles.route('/stations/fuel')
def fuel_data():
    refueling_data = {}
    fuel_stations = FuelStation.query.all()
    for fuel_station in fuel_stations:
        name = fuel_station.display_name
        refuel_events = RefuelEvent.query.filter(station_id=fuel_station.id)
    return 'Ok'


