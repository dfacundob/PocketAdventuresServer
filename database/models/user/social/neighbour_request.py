from database.database import db


class NeighbourRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    receiver_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    def __repr__(self):
        return '<NeighbourRequest {}, {}>'.format(self.id, self.receiver_profile_id)
