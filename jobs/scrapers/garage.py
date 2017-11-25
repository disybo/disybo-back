import datetime

import config
from api.maintenance_data.models import GarageVisit
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

    def get_all_checkins(self):


        session = self.db.session
        all_ids = [x.vehicle_id for x in session.query(Vehicle).all()]

        for id in all_ids:
            resp = self.post(self.resource, {'Name': id})
            resp.raise_for_status()
            json = resp.json()
            if 'rows' in json:
             for row in json['rows']:
                vehicle_id = row.get('IMPCODE', '')
                try:
                    service_time = datetime.datetime.fromtimestamp(row.get('SERVD') / 1000)
                except Exception as ex:
                    print("Could not parse service time!")
                    pass
                try:
                    bill_time = datetime.datetime.fromtimestamp(row.get('BILLD') / 1000)
                except Exception as ex:
                    print("Could not parse bill time!")
                    pass
                note = row.get('NOTE', '')
                name = row.get('NAME', '')

                sehiid = row.get('SEHIID', '')
                rtype = row.get('RTYPE', 1.0)
                total_sum = row.get('TSUM', 0.0)
                item = row.get('ITEM', '')
                ssumnovat = row.get('SSUMNOVAT', 0.0)
                unitpr = row.get('UNIPTR', 0.0)

                visit = GarageVisit(
                    vehicle_id=vehicle_id,
                    service_time=service_time,
                    bill_time=bill_time,
                    note=note,
                    name=name,
                    sehiid=sehiid,
                    rtype=rtype,
                    total_sum=total_sum,
                    item=item,
                    ssumnovat=ssumnovat,
                    unitpr=unitpr
                )
                try:
                    session.add(visit)
                    session.commit()
                except Exception as e:
                    print("Caught {}".format(e))
                    pass


if __name__ == '__main__':
    scraper = GarageScraper()
    scraper.get_all_checkins()