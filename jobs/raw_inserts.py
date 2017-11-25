from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from jobs.scrapers.scrapers import DBConnector
from api.vehicle_station_data.models import FuelStation, FuelType, RefuelEvent, Vehicle
from sqlalchemy.sql import func
import config


def insert_fuel_stations():
    db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    session = db.session

    fuel_stations = [
        {'id': '001', 'name': 'Hernesaari', 'longitude': 0, 'latitude': 0},
        {'id': '002', 'name': 'Pitäjämäki', 'longitude': 0, 'latitude': 0},
        {'id': '003', 'name': 'Toukola', 'longitude': 0, 'latitude': 0},
        {'id': '004', 'name': 'Oulunkylä', 'longitude': 0, 'latitude': 0},
        {'id': '005', 'name': 'Malmi', 'longitude': 0, 'latitude': 0},
        {'id': '006', 'name': 'Roihuvuori', 'longitude': 0, 'latitude': 0},
        {'id': '007', 'name': 'Toukola', 'longitude': 0, 'latitude': 0}
    ]

    for fuel_station in fuel_stations:
        fs = FuelStation(station_id=fuel_station['id'],
                         display_name=fuel_station['name'],
                         long=fuel_station['longitude'],
                         lat=fuel_station['latitude'])
        if not session.query(exists().where(FuelStation.station_id == fs.station_id)).scalar():
            session.add(fs)
            print('Added fuelstation: ', fs.display_name)
    session.commit()


def insert_fuel_types():
    db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    session = db.session

    fuel_types = [
        {'stara_id': '0001', 'display_name': 'Diesel'},
        {'stara_id': '0002', 'display_name': 'polttoöljy'},
        {'stara_id': '0003', 'display_name': 'bensa'},
        {'stara_id': '0004', 'display_name': 'ADblue'},

    ]

    for fuel_type in fuel_types:
        ft = FuelType(stara_id=fuel_type['stara_id'],
                      display_name=fuel_type['display_name'])
        if not session.query(exists().where(FuelType.stara_id == ft.stara_id)).scalar():
            session.add(ft)
            print('Added fueltype: ', ft.display_name)
    session.commit()


def query_vehicles():
    db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    session = db.session
    json_list = []
    counter = 0
    for v in session.query(Vehicle.fuel_card_num).distinct():
        fuel_card_num = v[0]
        if fuel_card_num == 'None':
            continue
        cars = session.query(Vehicle).filter(Vehicle.fuel_card_num == fuel_card_num).all()
        if len(cars) > 1:
            continue
        car = cars[0]
        total_fuel = session.query(RefuelEvent).with_entities(func.sum(RefuelEvent.fuel_volume).label('sum')).filter(
            RefuelEvent.fuel_card_num == fuel_card_num
        ).scalar()

        data = {
            'id': car.id,
            'vehicle_id': car.vehicle_id,
            'description': car.description,
            'consumption': total_fuel
        }

        if data['consumption']:
            print(data)
            counter += 1

        if counter == 10:
            break


if __name__ == '__main__':
    # insert_fuel_stations()
    # insert_fuel_types()
    query_vehicles()
