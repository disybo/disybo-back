import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from api.vehicle_data.models import Vehicle, FuelCardNumber, VehicleType
from common.globals import STARA_API_BASE

class DBConnector(object):
    engine = None
    session = None

    def __init__(self, uri):
        self.engine = create_engine(uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


""" Scrapes an API and returns the JSON data """
class StaraAPIScraper(object):
    app_key = ""
    base_url = ""
    headers = {}

    def __init__(self, base_url=STARA_API_BASE, app_key='f848dba8-adc9-45e5-9771-b51b0ffa700a'):
        self.base_url = base_url
        self.app_key = app_key
        self.headers = {
            'appKey': self.app_key,
            'x-thingworx-session': 'true',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get(self, resource, payload=None):
        if payload is None:
            payload = {}
        r = requests.get(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        return r

    def post(self, resource, payload=None):
        if payload is None:
            payload = {}
        r = requests.post(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        return r

class VehicleScraper(StaraAPIScraper):
    resource = "Vehicles"
    db = None

    def __init__(self):
        super().__init__()
        self.db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

    def bootstrap(self):
        session = self.db.session
        data = {
            'B1': 'Car',
            'B2': 'Van',
            'A3': 'Truck',
            'A4': 'Multi-function truck',
            'A6': 'Exchangable carriages, Addons',
            '14': 'Shovel',
            '47': 'Forklift',
            '51': 'Tractor 4-wheel drive',
            '52': 'Wheel loader',
            '53': 'Multi function device',
            '56': 'Grader',
            '78': 'Harvester',
            '87': 'Level cutter, other driving cutters',
            '88': 'Garden machines, pick-up trucks',
            '95': 'Grass cutter'
        }
        for vehicle_type in data:
            vt = VehicleType(stara_id=vehicle_type, display_name=data[vehicle_type])
            session.add(vt)
        session.commit()

    def get_all_vehicles(self):
        resp = self.post(self.resource)
        resp.raise_for_status()
        vehicles_json = resp.json()

        fuel_card_nums = set()
        vehicles = []
        vehicle_types = []

        session = self.db.session

        for v in vehicles_json['rows']:
            if 'FuelCardNum' in v:
                fcn = v['FuelCardNum']
                fuel_card_nums.add(fcn)

            if 'Name' in v and len(v['Name']) is 6:
                vehicle_id = v['Name']
                description = v.get('Description', '')

                (t, y, n) = [ vehicle_id[i : i + 2] for i in range(3) ]

                vehicle = Vehicle(vehicle_id=vehicle_id,
                                  fuel_card_num=v.get('FuelCardNum', None),
                                  description=description,
                                  type=t,
                                  year=y,
                                  num=n)
                vehicle_type = VehicleType(stara_id=vehicle_id, )
                vehicles.append(vehicle)

        existing_vehicles = set(session.query(Vehicle.vehicle_id).all())
        existing_fcn = set(session.query(FuelCardNumber.num).all())

        for fcn in fuel_card_nums:
            if fcn not in existing_fcn:
                session.add(FuelCardNumber(num=fcn))
        session.commit()

        for v in vehicles:
            if v.vehicle_id not in existing_vehicles:
                session.add(v)
        session.commit()


if __name__ == '__main__':
    scraper = VehicleScraper()
    # scraper.get_all_vehicles()
    scraper.bootstrap()
