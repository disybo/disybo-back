from flask import Blueprint, request, Response, jsonify
from api.vehicle_station_data.models import FuelStation, RefuelEvent, Boy
from datetime import datetime
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


@stations.route('/fuel/overall/<string:request_start_date>/<string:request_end_date>')
def get_overall_consumption(request_start_date, request_end_date):
    # request_start_date = request.args.get('start_date')
    # request_end_date = request.args.get('end_date')
    # granularity = request.args.get('granularity')

    start_date = datetime.strptime(request_start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(request_end_date.split('T')[0], '%Y-%m-%d')

    refuels = RefuelEvent.query.filter(
        RefuelEvent.time.between(start_date, end_date)
    ).all()

    json_list = []
    for rf in refuels:
        json_list.append({'id': rf.id,
                          'station_id': rf.station_id,
                          'fuel_card_num': rf.fuel_card_num,
                          'fuel_type': rf.fuel_type,
                          'km': rf.km,
                          'time': rf.time.isoformat()
                          })

    return Response(json.dumps(json_list), mimetype='application/json')


@stations.route('/')
def get_all_stations():
    station_list = FuelStation.query.all()

    json_list = []

    for station in station_list:
        json_list.append({"id": station.id, "display_name": station.display_name})

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')


