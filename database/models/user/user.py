from datetime import datetime, timedelta

from database.database import db
from database.models.user.profile import UserProfile


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, unique=True)

    unique_identifier = db.Column(db.String(100), nullable=False)
    locale = db.Column(db.String(100), nullable=False)
    last_command_count = db.Column(db.Integer, nullable=False, default=-1)
    last_command_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(100), nullable=False, default='')

    # admin stuff
    is_banned = db.Column(db.Boolean, nullable=False, default=False)
    ban_end_time = db.Column(db.DateTime, nullable=True)
    ban_reason = db.Column(db.String(100), nullable=True)
    emulated_at = db.Column(db.DateTime, nullable=True)
    emulation_start_date = db.Column(db.DateTime, nullable=True)
    emulated_user_id = db.Column(db.String(100), nullable=True)

    profile = db.relationship('UserProfile', uselist=False, backref='User')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.profile is None:
            self.profile = UserProfile(id=self.id)  # Avoid non synchronized user & profile id

        else:
            print('{} already has an userprofile'.format(self))

    @property
    def is_online(self):
        return self.last_command_time + timedelta(minutes=6) > datetime.utcnow()

    @property
    def is_emulated(self):
        if self.emulated_at is not None:
            return self.emulated_at + timedelta(minutes=30) > datetime.utcnow()

        else:
            return False

    def __repr__(self):
        return '<User {}, {}>'.format(self.id, self.unique_identifier)
