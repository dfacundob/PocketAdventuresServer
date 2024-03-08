from database.database import db


class BunkerShip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bunker_id = db.Column(db.Integer, db.ForeignKey('bunker.id', ondelete='CASCADE'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<BunkerShip {}, {}>'.format(self.id, self.sku)
