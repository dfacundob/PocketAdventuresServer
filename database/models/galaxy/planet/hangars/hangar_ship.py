from database.database import db


class HangarShip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hangar_id = db.Column(db.Integer, db.ForeignKey('hangar.id', ondelete='CASCADE'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<HangarShip {}, {}>'.format(self.id, self.sku)
