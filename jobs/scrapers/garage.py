import config
from api.vehicle_data.models import Vehicle, FuelCardNumber, VehicleType
from jobs.scrapers.scrapers import StaraAPIScraper, DBConnector


class GarageScraper(StaraAPIScraper):
    resource = "Garage"
    db = None

    def __init__(self):
        super().__init__()
        self.db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

    def bootstrap(self):
        session = self.db.session
        """
            {
         "TSUM": 767.94,
         "ITEM": "T3",
         "NOTE": "",
         "RTYPE": 7,
         "NUM": 3.8,
         "SSUMNOVAT": 411.88,
         "BILLD": 1494288000000,
         "IMPCODE": "A30806",
         "SERVD": 1487329620000,
         "SEHIID": 17483,
         "UNITPR": 108.39,
         "NAME": "ILMAPUSSIN VAIHTO"
       },
        """

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
