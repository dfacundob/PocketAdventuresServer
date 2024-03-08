from database.database import db


class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Flag {}, {}>'.format(self.id, self.key)
