from collections import defaultdict
from flask import Blueprint, Response
import json
from .models import Boy, Vehicle, VehicleType, RefuelEvent, FuelStation, FuelType, VehicleFuelConsumption
from api import MaintenancePeriod, Notification


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
    vehicle_list = Vehicle.query.limit(100)
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


@vehicles.route('/fuel/ratio')
def fuel_ratio():
    print('ok')


@vehicles.route('/fuel/total_consumption')
def fuel_per_car():
    fuel_consumptions = VehicleFuelConsumption.query.all()
    json_list = []

    for vfc in fuel_consumptions:
        json_list.append(
            {'id': vfc.id,
             'vehicle_id': vfc.vehicle_id,
             'fuel_card_num': vfc.fuel_card_num,
             'description': vfc.description,
             'consumption': vfc.consumption
             }
        )

    return Response(json.dumps(json_list), mimetype='application/json')


@vehicles.route('/stations/fuel')
def fuel_data():
    refueling_data = {}

    fuel_stations = FuelStation.query.all()
    for fuel_station in fuel_stations:
        name = fuel_station.display_name
        refuel_events = RefuelEvent.query.filter(station_id=fuel_station.id)
    return 'Ok'


@vehicles.route('/alerts')
def alerts():
    from database import db
    from sqlalchemy import func
    alerts = [x.as_dict() for x in db.session.query(Notification).order_by(func.random()).limit(20)]
    # alerts.append({
    #     "vehicle_type": "B2",
    #     "urgency": "high",
    #     "vehicle_id": "B21601",
    #     "description": "20km (3 days) until recommended maintenance"
    # })
    # alerts.append({
    #     "vehicle_type": "B1",
    #     "urgency": "low",
    #     "vehicle_id": "B19903",
    #     "description": "80km (20 days) until recommended maintenance"
    # })
    # alerts.append({
    #     "vehicle_type": "73",
    #     "urgency": "medium",
    #     "vehicle_id": "731102",
    #     "description": "16km (7 days) until recommended maintenance"
    # })
    return Response(json.dumps(alerts), mimetype='application/json')
