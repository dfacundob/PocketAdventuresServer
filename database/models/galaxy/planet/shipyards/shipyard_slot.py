from database.database import db


class ShipyardSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipyard_id = db.Column(db.Integer, db.ForeignKey('shipyard.id', ondelete='CASCADE'), nullable=False)

    ships_sku = db.Column(db.String(100))

    ships = db.relationship('ShipyardShip', backref='Shipyardslot', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<ShipyardSlot {}, {}>'.format(self.id, self.ships_sku)
