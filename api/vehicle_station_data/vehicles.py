from collections import defaultdict

from flask import Blueprint, Response
import json
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


@vehicles.route('/')
def get_all_vehicles():
    vehicle_list = Vehicle.query.all()
    vehicle_types_list = VehicleType.query.all()

    vehicle_types_dict = defaultdict()

    for vehicle_type in vehicle_types_list:
        vehicle_types_dict[vehicle_type.stara_id] = vehicle_type.display_name

    json_list = []

    for vehicle in vehicle_list:
        json_list.append({"id": vehicle.id, "vehicle_id": vehicle.vehicle_id, "description": vehicle.description,
                          "type": vehicle_types_dict[vehicle.type]})

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')


@vehicles.route('/stations/fuel')
def fuel_data():
    refueling_data = {}

    fuel_stations = FuelStation.query.all()
    for fuel_station in fuel_stations:
        name = fuel_station.display_name
        refuel_events = RefuelEvent.query.filter(station_id=fuel_station.id)
    return 'Ok'


