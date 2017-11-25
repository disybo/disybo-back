from sqlalchemy.orm import relationship

from api.vehicle_station_data.models import Vehicle, VehicleType
from database import db


class GarageVisit(db.Model):
    __tablename__ = 'garage_visits'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(6), db.ForeignKey(Vehicle.__table__.columns.vehicle_id))
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

    vehicle_rel = relationship(Vehicle, foreign_keys=[vehicle_id])

class MaintenanceKM(db.Model):
    __tablename__ = 'maint_km'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, db.ForeignKey(VehicleType.__table__.columns.stara_id))
    km_thresh = db.Column(db.Float)
    days_thresh = db.Column(db.Integer)

    type_rel = relationship(VehicleType, foreign_keys=[type])

