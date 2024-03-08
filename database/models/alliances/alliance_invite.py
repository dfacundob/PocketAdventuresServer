from datetime import datetime, timedelta

from database.database import db


class AllianceInvite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    receiver_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    type = db.Column(db.Integer, nullable=False)
    alliance_id = db.Column(db.Integer, nullable=False)
    alliance_name = db.Column(db.String(100), nullable=False)

    sent_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def sent_at(self):
        return int(self.sent_date.timestamp() * 1000)

    @property
    def expiry_time(self):
        return int((self.sent_date + timedelta(days=3)).timestamp() * 1000)

    def __repr__(self):
        return '<AllianceInvite {}, {}>'.format(self.id, self.sent_date)
