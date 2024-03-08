from database.database import db


class Neighbour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    friend_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Neighbour {}, {}>'.format(self.id, self.friend_id)
