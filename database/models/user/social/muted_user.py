from database.database import db


class MutedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<MutedUser {}, {}>'.format(self.id, self.user_id)
