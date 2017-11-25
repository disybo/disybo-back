from flask import Blueprint, request, Response, jsonify
from api.vehicle_station_data.models import FuelStation, RefuelEvent, Boy
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


@stations.route('/fuel/overall/')
def get_overall_consumption():
    start_date = 'Fri Jan 01 2016 00:00:00 GMT+0200 (EET)'
    end_date = 'Sun Jan 01 2017 00:00:00 GMT+0200'

    date_format = 'YYYY-MM-DD'

    print('2016-02-02 12:01:00' > 'Fri Jan 01 2016 00:00:00 GMT+0200 (EET)')

    refuel_events = RefuelEvent.query.all()

    print(len(refuel_events))

    return Response()





@stations.route('/')
def get_all_stations():
    station_list = FuelStation.query.all()

    json_list = []

    for station in station_list:
        json_list.append({"id": station.id, "display_name": station.display_name})
        print(station.display_name)

    # then do this
    return Response(json.dumps(json_list), mimetype='application/json')




