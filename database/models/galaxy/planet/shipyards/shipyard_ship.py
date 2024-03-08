from datetime import datetime
from database.database import db


class ShipyardShip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('shipyard_slot.id', ondelete='CASCADE'), nullable=False)

    end_time = db.Column(db.DateTime, nullable=False)

    @property
    def time_left(self):
        return max(0, int((self.end_time - datetime.utcnow()).total_seconds() * 1000))

    def __repr__(self):
        return '<ShipyardShip {}, {}>'.format(self.id, self.slot_id)
