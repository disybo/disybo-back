"""
Background job for processing fleet maintenance data and generating alerts depending on status
"""
from sqlalchemy import func

import config
from api import MaintenancePeriod, Vehicle, RefuelEvent, GarageVisit, Notification
from jobs.scrapers.scrapers import DBConnector

if __name__ == '__main__':
    db = DBConnector(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    """

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, db.ForeignKey(VehicleType.__table__.columns.stara_id))
    km_thresh = db.Column(db.Float)
    days_thresh = db.Column(db.Integer)
    """
    maint_periods = db.session.query(MaintenancePeriod).all()
    print(maint_periods)
    thresholds = {}
    for period in maint_periods:
        thresholds[period.type] = {
            'km': period.km_thresh,
            'days': period.days_thresh
        }

    for limit in maint_periods:
        latest_services = (
            db.session.query(GarageVisit.vehicle_id, Vehicle.fuel_card_num,
                             func.max(GarageVisit.service_time).label('service_time'))
                .join(Vehicle)
                .filter(Vehicle.fuel_card_num != None)
                .filter(Vehicle.vehicle_id == GarageVisit.vehicle_id)
                .group_by(GarageVisit.vehicle_id, Vehicle.fuel_card_num)
        ).all()

        for s in latest_services:
            t = s.vehicle_id[0:2]
            time = s.service_time

            print(t)
            print(time)
            # Determine how many KM driven since last check
            distances = (db.session.query(func.array_agg(RefuelEvent.km), func.array_agg(RefuelEvent.time))
                         .filter(RefuelEvent.fuel_card_num == s.fuel_card_num)
                         .filter(RefuelEvent.time > time)
                         .group_by(RefuelEvent.fuel_card_num)
                         .first()
                         )
            print("All done")
            if distances:
                driven_km = max(distances[0]) - min(distances[0])
                driven_time = max(distances[1]) - min(distances[1])

                if driven_km and driven_time:
                    print("Driven {}km ({} days))".format(driven_km, driven_time.days))
                    if thresholds.get(t):
                        vehicle_type = t
                        vehicle_id = s.vehicle_id
                        urgency = None
                        description = "(None)"

                        template = "{}km until recommended maintenance"

                        thresh_km = thresholds[t]['km']
                        thresh_dur = thresholds[t]['days']
                        if driven_km >= thresh_km:
                            urgency = "urgent"
                            description = "This vehicle is overdue for its scheduled maintenance ({}km of recommended {}km)".format(
                                driven_km, thresh_km)
                        elif driven_km >= 0.9 * thresh_km:
                            urgency = "high"
                            description = template.format(thresh_km - driven_km, thresh_km)
                        elif driven_km >= 0.7 * thresh_km:
                            urgency = "medium"
                            description = template.format(thresh_km - driven_km, thresh_km)
                        elif driven_km >= 0.5 * thresh_km:
                            urgency = "low"
                            description = template.format(thresh_km - driven_km, thresh_km)

                        if urgency:
                            alert = Notification(urgency=urgency, description=description, vehicle_id=vehicle_id,
                                                 type=vehicle_type)
                            print("Adding {}".format(alert))
                            db.session.add(alert)
                            db.session.commit()
