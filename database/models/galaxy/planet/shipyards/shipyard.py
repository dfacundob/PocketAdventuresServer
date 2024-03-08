from database.database import db
from database.models.galaxy.planet.shipyards.shipyard_slot import ShipyardSlot


class Shipyard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    sid = db.Column(db.Integer, nullable=False)
    unlocked_slots = db.Column(db.Integer, nullable=False, default=0)

    slots = db.relationship('ShipyardSlot', backref='Shipyard', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.slots.all():
            for _ in range(3):
                self.slots.append(ShipyardSlot())

    def __repr__(self):
        return '<Shipyard {}, {}>'.format(self.id, self.sid)
