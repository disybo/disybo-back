from database import db


# TODO Could this be better off as an ENUM?
class VehicleType(db.Model):
    __tablename__ = 'vehicle_types'

    id = db.Column(db.Integer, primary_key=True)
    stara_id = db.Column(db.Integer)
    display_name = db.Column(db.String)


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(6))
    fuel_card_num = db.Column(db.String())
    description = db.Column(db.String())
    type = db.Column(db.Integer, db.ForeignKey(VehicleType.__table__.columns.id))
    year = db.Column(db.Integer)
    num = db.Column(db.Integer)
