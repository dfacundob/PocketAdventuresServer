from datetime import datetime
from database.database import db


class GameUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    unlocked = db.Column(db.Boolean, nullable=False, default=False)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    upgrade_id = db.Column(db.Integer, nullable=False, default=0)
    is_upgrading = db.Column(db.Boolean, nullable=False, default=True)

    def encode(self):
        game_unit_info = {}

        game_unit_info['sku'] = self.sku
        game_unit_info['unlocked'] = self.unlocked
        game_unit_info['upgradeId'] = self.upgrade_id
        game_unit_info['timeLeft'] = self.time_left

        return game_unit_info

    @property
    def time_left(self):
        if self.is_upgrading:
            return max(0, int((self.end_time - datetime.utcnow()).total_seconds() * 1000))

        else:
            return -1

    def __repr__(self):
        return '<GameUnit {}, {}>'.format(self.id, self.sku)
