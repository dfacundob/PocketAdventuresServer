from database.database import db


class Bunker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    sid = db.Column(db.Integer, nullable=False)
    bunker_ships = db.relationship('BunkerShip', backref='Bunker', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Bunker {}, {}>'.format(self.id, self.sid)
