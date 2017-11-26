"""
This script performs data fetching jobs related to fleet maintenance
"""

from sqlalchemy import func

import config
from api import GarageVisit, Vehicle, RefuelEvent, MaintenancePeriod
from jobs.scrapers.scrapers import DBConnector

SERVICE_QUERY = "SELECT service_time, vehicle_id FROM garage_visits GROUP BY vehicle_id, service_time, sehiid ORDER BY vehicle_id, service_time LIMIT 10;"

if __name__ == '__main__':
    db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

    # Get service dates for vehicles/fuel card #s
    service_data = (db.session.query(GarageVisit.vehicle_id, Vehicle.fuel_card_num,
                                     func.array_agg(func.distinct(GarageVisit.service_time)).label('service_time'))
                    .join(Vehicle)
                    .filter(Vehicle.fuel_card_num != None)
                    .filter(Vehicle.vehicle_id == GarageVisit.vehicle_id)
                    .order_by(GarageVisit.vehicle_id)
                    .group_by(GarageVisit.vehicle_id, Vehicle.fuel_card_num)
                    ).all()


    def find_nearest(x, a):
        pass
        for i in range(len(x)):
            if x[i].time > a:
                return x[i]


    # Loop over service points to determine nearest refueling points
    averages = {}
    average_km = {}
    average_dur = {}
    for rec in service_data:
        fcn = rec.fuel_card_num
        st = rec.service_time
        vid = rec.vehicle_id

        # For each service time in 'st', find closest refueling point and measure average KM driven between servicing
        distances = (db.session.query(RefuelEvent.km, RefuelEvent.time)
                     .filter(RefuelEvent.fuel_card_num == fcn)
                     .order_by(RefuelEvent.time)
                     ).all()
        if len(distances) == 0:
            continue

        last_km = 0
        last_time = st[0]
        tot = 0
        tot_dur = 0

        for service_time in st:
            nearest = find_nearest(distances, service_time)
            if nearest is not None:
                tot_dur += (nearest.time - last_time).days
                tot += (nearest.km - last_km)
                last_km = nearest.km
                last_time = nearest.time

        avg = (tot / len(st), tot_dur / len(st))
        print(avg)
        vehicle_type = vid[0:2]
        cur = averages.get(vehicle_type, ([], []))
        cur[0].append(avg[0])
        cur[1].append(avg[1])
        averages[vehicle_type] = cur

    # Compute averages and push to DB
    for thing in averages:
        (akm, at) = averages[thing]
        print("{}: {}, {}".format(thing, akm, at))
        avg_km = sum(akm) / len(akm)
        avg_day = sum(at) / len(at)
        m = MaintenancePeriod(type=thing, km_thresh=avg_km, days_thresh=avg_day)
        db.session.add(m)
    db.session.commit()
