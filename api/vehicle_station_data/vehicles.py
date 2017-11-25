from flask import Blueprint, Response
from .models import Boy, Vehicle, VehicleType
import json
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

    json_list = []

    for vehicle in vehicle_list:
        json_list.append({"id": vehicle.id, "vehicle_id": vehicle.vehicle_id, "description": vehicle.description,
                          "type": VehicleType.query.get(vehicle.type).display_name})

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')
