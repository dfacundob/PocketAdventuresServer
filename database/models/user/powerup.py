from datetime import datetime
from database.database import db


class PowerUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def time_left(self):
        return max(0, int((self.end_time - datetime.utcnow()).total_seconds() * 1000))

    def __repr__(self):
        return '<PowerUp {}, {}>'.format(self.id, self.sku)
