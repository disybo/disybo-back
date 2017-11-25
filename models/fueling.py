from database import db

from models.vehicle import Vehicle


# TODO Could this be better off as an ENUM?
class FuelType(db.Model):
    __tablename__ = 'fuel_types'

    id = db.Column(db.Integer, primary_key=True)
    stara_id = db.Column(db.String)
    display_name = db.Column(db.String)


class FuelStation(db.Model):
    __tablename__ = 'fuel_stations'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String())
    display_name = db.Column(db.String())
    long = db.Column(db.Float)
    lat = db.Column(db.Float)


class RefuelEvent(db.Model):
    __tablename__ = 'refuel_events'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey(FuelStation.__table__.columns.id))
    fuel_card_num = db.Column(db.String(), db.ForeignKey(Vehicle.__table__.columns.fuel_card_num))
    fuel_type = db.Column(db.Integer, db.ForeignKey(FuelType.__table__.columns.id))
    fuel_volume = db.Column(db.Float)
    km = db.Column(db.Integer)
    time = db.Column(db.DateTime)
