from datetime import datetime, timedelta
from database.database import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sender_id = db.Column(db.Integer, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() - timedelta(hours=2))

    def __repr__(self):
        return '<Message {}, {}>'.format(self.id, self.time)
