from datetime import datetime, timedelta

from database.database import db


class AllianceShip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    expire_at = db.Column(db.BigInteger, nullable=False, default=lambda: int((datetime.utcnow() + timedelta(days=1)).timestamp() * 1000))

    def encode(self):
        ship_info = {}

        ship_info['sku'] = self.sku
        ship_info['amount'] = self.amount
        ship_info['time'] = self.expire_at
        ship_info['created'] = self.expire_at - timedelta(days=1).total_seconds() * 1000

        return ship_info

    def __repr__(self):
        return '<AllianceShip {}, {}>'.format(self.id, self.sku)
