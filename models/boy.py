from database import db


class Boy(db.Model):
    __tablename__ = 'boys'

    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String())
    name = db.Column(db.String())

    def __init__(self, role, name):
        self.role = role
        self.name = name

    def __repr__(self):
        return '<user id {}>'.format(self.user_id)
