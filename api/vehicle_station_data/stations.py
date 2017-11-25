from flask import Blueprint, request, Response, jsonify
from api.vehicle_station_data.models import FuelStation, RefuelEvent, Boy
from datetime import datetime
from sqlalchemy.sql import func
from database import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
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


@stations.route('/fuel/granular')
def get_granular_consumption():
    request_start_date = request.args.get('start')
    request_end_date = request.args.get('end')

    start_date = datetime.strptime(request_start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(request_end_date.split('T')[0], '%Y-%m-%d')

    # granularity = request.args.get('granularity')
    granularity = 'monthly'

    json_list = []

    if granularity == 'monthly':
        granular_start_date = start_date.replace(day=1)
        last_day = calendar.monthrange(end_date.year, end_date.month)
        granular_end_date = end_date.replace(day=last_day[1])

        fuel_stations = FuelStation.query.all()

        for fs in fuel_stations:
            month_index = 0
            station_info = {'station_id': fs.station_id,
                            'display_name': fs.display_name,
                            'fuel_data': []}
            granular_start_date = start_date.replace(day=1)
            while granular_start_date < granular_end_date:
                next_date = granular_start_date + relativedelta(months=1)
                refuel_sum = RefuelEvent.query.with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
                    RefuelEvent.station_id == fs.station_id,
                    RefuelEvent.time.between(granular_start_date, next_date)
                ).scalar()
                station_info['fuel_data'].append({'month': month_index, 'fuel_volume': refuel_sum })
                granular_start_date = next_date
                month_index += 1
            json_list.append(station_info)
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




