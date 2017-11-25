from database import db


class GarageVisit(db.Model):
    __tablename__ = 'garage_visits'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(6))
    service_time = db.Column(db.DateTime)
    bill_time = db.Column(db.DateTime)
    note = db.Column(db.String())
    name = db.Column(db.String())

    # TODO Research what these are
    sehiid = db.Column(db.Integer)
    rtype = db.Column(db.Float)
    total_sum = db.Column(db.Float)
    item = db.Column(db.String())
    ssumnovat = db.Column(db.Float)
    unitpr = db.Column(db.Float)
