from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from jobs.scrapers.scrapers import DBConnector
from api.vehicle_data.models import FuelStation
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

if __name__ == '__main__':
    insert_fuel_stations()
