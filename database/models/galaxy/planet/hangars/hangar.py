from database.database import db


class Hangar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    sid = db.Column(db.Integer, nullable=False)
    hangar_ships = db.relationship('HangarShip', backref='Hangar', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Hangar {}, {}>'.format(self.id, self.sid)
