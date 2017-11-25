from flask import Blueprint, request, Response, jsonify
from api.vehicle_station_data.models import FuelStation, RefuelEvent, Boy, FuelType
from datetime import datetime
from sqlalchemy.sql import func
from database import db
from datetime import datetime
import json

stations = Blueprint('stations', 'stations', url_prefix='/api/stations')


@stations.route('/boys/<int:user_id>')
def hello_world(user_id):
    try:
        name = Boy.query.get(user_id).name
        return "<h1>Hello, {}</ht>".format(name)
    except Exception as ex:
        print(ex)
        return '<h1>Something is broken.</h1>'


@stations.route('/fuel/overall')
def get_overall_consumption():
    request_start_date = request.args.get('start')
    request_end_date = request.args.get('end')
    # granularity = request.args.get('granularity')

    start_date = datetime.strptime(request_start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(request_end_date.split('T')[0], '%Y-%m-%d')

    json_list = []
    fuel_stations = FuelStation.query.all()

    for fs in fuel_stations:
        refuel_sum = RefuelEvent.query.with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
            RefuelEvent.station_id == fs.station_id,
            RefuelEvent.time.between(start_date, end_date)
        ).scalar()
        json_list.append(
            {'station_id': fs.station_id,
             'display_name': fs.display_name,
             'fuel_volume': refuel_sum}
        )
    return Response(json.dumps(json_list), mimetype='application/json')


@stations.route('/fuel/type')
def get_fuel_type():
    request_start_date = request.args.get('start')
    request_end_date = request.args.get('end')
    # granularity = request.args.get('granularity')

    start_date = datetime.strptime(request_start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(request_end_date.split('T')[0], '%Y-%m-%d')

    json_list = []
    fuel_stations = FuelStation.query.all()
    fuel_types = FuelType.query.all()

    for fs in fuel_stations:
        fuel_sums = []
        for fuel in fuel_types:
            fuel_sum = RefuelEvent.query.with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
                RefuelEvent.fuel_type == fuel.id,
                RefuelEvent.station_id == fs.station_id,
                RefuelEvent.time.between(start_date, end_date)
            ).scalar()
            fuel_sums.append({"fuel_name": fuel.display_name, "amount": fuel_sum})
        json_list.append(
            {'station_id': fs.station_id,
             'display_name': fs.display_name,
             'fuel_volume': fuel_sums}
        )
    return Response(json.dumps(json_list), mimetype='application/json')


@stations.route('/')
def get_all_stations():
    station_list = FuelStation.query.all()

    json_list = []

    for station in station_list:
        json_list.append({"id": station.id, "display_name": station.display_name})
        print(station.display_name)

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')




