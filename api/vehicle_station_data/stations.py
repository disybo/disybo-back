from flask import Blueprint, request, Response, jsonify
from api.vehicle_station_data.models import FuelStation, RefuelEvent, Boy
from database import db
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


@stations.route('/fuel/overall/')
def get_overall_consumption():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    granularity = request.args.get('granularity')


@stations.route('/')
def get_all_stations():
    station_list = FuelStation.query.all()

    json_list = []

    for station in station_list:
        json_list.append({"id": station.id, "display_name": station.display_name})

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')


