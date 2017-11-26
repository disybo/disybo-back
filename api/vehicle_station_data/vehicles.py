import json
from collections import defaultdict
from flask import Blueprint, Response, request
from sqlalchemy.sql import func
from sqlalchemy import exists
import json
from api.vehicle_station_data.models import Vehicle, VehicleType, RefuelEvent, FuelStation, FuelType, \
    VehicleFuelConsumption
from api import MaintenancePeriod, Notification
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from api import Notification

vehicles = Blueprint('vehicles', 'vehicles', url_prefix='/api/vehicles')


@vehicles.route('/types')
def get_car_types():
    vehicle_types = VehicleType.query.all()

    json_list = []

    for vehicle_type in vehicle_types:
        if vehicle_type.display_name != "N/A":
            json_list.append({"id": vehicle_type.stara_id, "display_name": vehicle_type.display_name})
    return Response(json.dumps(json_list), mimetype='application/json')


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


@vehicles.route('/fuel/consumption/type')
def fuel_per_vehicle_type():
    print('wat')
    vehicle_type_id = request.args.get('id')
    vehicle_type = VehicleType.query.filter(VehicleType.stara_id == vehicle_type_id).all()[0]

    vehicles_fcns = [x[0] for x in Vehicle.query.with_entities(Vehicle.fuel_card_num).filter(Vehicle.type == vehicle_type_id)]
    all_fcns = [x[0] for x in RefuelEvent.query.with_entities(RefuelEvent.fuel_card_num)]
    fuel_card_nums = list(set(vehicles_fcns).intersection(set(all_fcns)))

    print(len(fuel_card_nums))

    end_date = datetime.today()
    start_date = end_date - relativedelta(years=1)

    json_list = []

    last_day = calendar.monthrange(end_date.year, end_date.month)
    granular_end_date = end_date.replace(day=last_day[1])

    refill_info = {'vehicle_type': vehicle_type.display_name,
                   'fuel_data': []}
    granular_start_date = start_date.replace(day=1)
    print('query time')
    while granular_start_date < granular_end_date:
        next_date = granular_start_date + relativedelta(months=1)
        refuel_sum = RefuelEvent.query.with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
            RefuelEvent.fuel_card_num.in_(fuel_card_nums),
            RefuelEvent.time.between(granular_start_date, next_date)
        ).scalar()
        if refuel_sum:
            refill_info['fuel_data'].append({'month': granular_start_date.isoformat(), 'fuel_volume': refuel_sum})
        else:
            refill_info['fuel_data'].append({'month': granular_start_date.isoformat(), 'fuel_volume': 0})
        granular_start_date = next_date
    json_list.append(refill_info)
    return Response(json.dumps(json_list), mimetype='application/json')


@vehicles.route('/fuel/consumption/<string:vehicle_id>')
def fuel_per_vehicle(vehicle_id):
    end_date = datetime.today()
    start_date = end_date - relativedelta(years=1)

    granularity = 'monthly'

    json_list = []

    if granularity == 'monthly':
        granular_start_date = start_date.replace(day=1)
        last_day = calendar.monthrange(end_date.year, end_date.month)
        granular_end_date = end_date.replace(day=last_day[1])

        vehicle = Vehicle.query.filter(Vehicle.id == vehicle_id)[0]
        vfc_res = VehicleFuelConsumption.query.filter(VehicleFuelConsumption.vehicle_id == vehicle.vehicle_id).all()
        if len(vfc_res) == 1:
            vfc = vfc_res[0]

            vfc_info = {'_id': vehicle_id,
                        'vehicle_id': vfc.vehicle_id,
                        'description': vfc.description,
                        'fuel_data': []}
            granular_start_date = start_date.replace(day=1)
            while granular_start_date < granular_end_date:
                next_date = granular_start_date + relativedelta(months=1)

                refuel_sum = RefuelEvent.query.with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
                    RefuelEvent.fuel_card_num == vfc.fuel_card_num,
                    RefuelEvent.time.between(granular_start_date, next_date)
                ).scalar()
                if refuel_sum:
                    vfc_info['fuel_data'].append({'month': granular_start_date.isoformat(), 'fuel_volume': refuel_sum})
                else:
                    vfc_info['fuel_data'].append({'month': granular_start_date.isoformat(), 'fuel_volume': 0})
                granular_start_date = next_date
            json_list.append(vfc_info)
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
