import config
from api.vehicle_data.models import Vehicle, FuelCardNumber, VehicleType
from jobs.scrapers.scrapers import StaraAPIScraper, DBConnector


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
            try:
                vt = VehicleType(stara_id=vehicle_type, display_name=data[vehicle_type])
                session.add(vt)
                session.commit()
            except:
                pass

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

                (t, y, n) = [vehicle_id[i: i + 2] for i in range(0, 6, 2)]

                vehicle = Vehicle(vehicle_id=vehicle_id,
                                  fuel_card_num=v.get('FuelCardNum', None),
                                  description=description,
                                  type=t,
                                  year=y,
                                  num=n)
                vehicles.append(vehicle)
                vehicle_types.append(t)

        existing_vehicles = set([x.vehicle_id for x in session.query(Vehicle.vehicle_id).all()])
        existing_vtypes = set([x.stara_id for x in session.query(VehicleType.stara_id).all()])
        existing_fcn = set(session.query(FuelCardNumber.num).all())

        for fcn in fuel_card_nums:
            if fcn not in existing_fcn:
                try:
                    session.add(FuelCardNumber(num=fcn))
                    session.commit()
                except:
                    pass

        for v in vehicles:
            if v.type not in existing_vtypes:
                try:
                    session.add(VehicleType(stara_id=v.type, display_name='N/A'))
                    session.commit()
                except:
                    pass
            if v.vehicle_id not in existing_vehicles:
                try:
                    session.add(v)
                    session.commit()
                except:
                    pass
