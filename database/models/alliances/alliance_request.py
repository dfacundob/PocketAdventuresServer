from datetime import datetime, timedelta

from database.database import db


class AllianceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id', ondelete='CASCADE'), nullable=False)

    user_id = db.Column(db.Integer, nullable=False)
    sent_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def sent_at(self):
        return int(self.sent_date.timestamp() * 1000)

    @property
    def expiry_time(self):
        return int((self.sent_date + timedelta(days=3)).timestamp() * 1000)

    def __repr__(self):
        return '<AllianceRequest {}, {}>'.format(self.id, self.alliance_id)
