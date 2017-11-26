import config
from datetime import datetime
from api.vehicle_data.models import Vehicle, FuelCardNumber, VehicleType, RefuelEvent, FuelStation
from jobs.scrapers.scrapers import StaraAPIScraper, DBConnector


class RefuelScraper(StaraAPIScraper):
    resource = "Refuel"
    db = None

    def __init__(self):
        super().__init__()
        self.db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

    def bootstrap(self):
        session = self.db.session

    def get_all_refuels(self):
        session = self.db.session
        fuel_card_numbers = session.query(FuelCardNumber).all()

        fuel_station_ids = [x.station_id for x in session.query(FuelStation).all()]

        missing_ids = 0
        print(len(fuel_card_numbers))
        check = 1
        for fuel_card_number in fuel_card_numbers:
            resp = self.post(self.resource, {'FuelCardNum': fuel_card_number.num})
            resp.raise_for_status()
            refuel_json = resp.json()
            for rf in refuel_json['rows']:
                if rf['Station'] not in fuel_station_ids:
                    missing_ids += 1
                    continue
                parsed_time = datetime.fromtimestamp(int(rf['Time']) / 1000)
                refuel_event = RefuelEvent(station_id=rf['Station'],
                                           fuel_card_num=rf['FuelCardNum'],
                                           fuel_type=str(rf['FuelQuality']),
                                           fuel_volume=rf['FuelVolume'],
                                           km=rf['Km'],
                                           time=parsed_time
                                           )
                try:
                    session.add(refuel_event)
                except:
                    print('A single refuel transaction has failed')
            try:
                session.commit()
            except:
                print('A commit has failed.')
            print(check)
            check += 1

        print('Wrong ids attempts: ', missing_ids)


if __name__ == '__main__':
    refuel = RefuelScraper()
    refuel.get_all_refuels()
