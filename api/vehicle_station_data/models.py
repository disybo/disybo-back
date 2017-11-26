from sqlalchemy.orm import relationship

from database import db


# TODO Could this be better off as an ENUM?
class VehicleType(db.Model):
    __tablename__ = 'vehicle_types'
    stara_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String)


class FuelCardNumber(db.Model):
    __tablename__ = 'fuel_card_numbers'

    num = db.Column(db.String(), primary_key=True, autoincrement=False)


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(6), unique=True)
    fuel_card_num = db.Column(db.String(), db.ForeignKey(FuelCardNumber.__table__.columns.num))
    description = db.Column(db.String())
    type = db.Column(db.String, db.ForeignKey(VehicleType.__table__.columns.stara_id))
    year = db.Column(db.Integer)
    num = db.Column(db.Integer)

    # Relationships
    fuel_card_rel = relationship(FuelCardNumber, foreign_keys=[fuel_card_num])
    type_rel = relationship(VehicleType, foreign_keys=[type])


class VehicleFuelConsumption(db.Model):
    __tablename__ = 'vehicle_fuel_consumption'

    id = db.Column(db.Integer, primary_key=True)
    fuel_card_num = db.Column(db.String(), db.ForeignKey(FuelCardNumber.__table__.columns.num))
    vehicle_id = db.Column(db.String(6), db.ForeignKey(Vehicle.__table__.columns.vehicle_id))
    description = db.Column(db.String())
    consumption = db.Column(db.Float())


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
    fuel_card_num = db.Column(db.String(), db.ForeignKey(FuelCardNumber.__table__.columns.num))

    fuel_type = db.Column(db.Integer, db.ForeignKey(FuelType.__table__.columns.id))
    fuel_volume = db.Column(db.Float)
    km = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    # Relationships
    fuel_card_rel = relationship(FuelCardNumber, foreign_keys=[fuel_card_num])
