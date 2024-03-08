from datetime import datetime, timedelta

from database.database import db
from utils.utils import alliance_powerups


class AlliancePowerUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id', ondelete='CASCADE'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    contribution = db.Column(db.Integer, nullable=False, default=0)

    cooldown_end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activation_time_end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def encode(self):
        is_active = self.activation_time_end >= datetime.utcnow()

        powerup_info = {}

        powerup_info['sku'] = self.sku
        powerup_info['active'] = is_active
        powerup_info['contribution'] = self.contribution

        if is_active:
            powerup_info['activationTime'] = int(self.activation_time_end.timestamp() * 1000)

        else:
            if self.cooldown_end_time >= datetime.utcnow():
                powerup_info['coolDown'] = int(self.cooldown_end_time.timestamp() * 1000)

            else:
                powerup_info['coolDown'] = -1

        return powerup_info

    def activate(self):
        self.contribution -= alliance_powerups[self.sku]
        self.activation_time_end = datetime.utcnow() + timedelta(days=1)
        self.cooldown_end_time = datetime.utcnow() + timedelta(days=4)

    def __repr__(self):
        return '<AlliancePowerUp {}, {}>'.format(self.id, self.sku)
