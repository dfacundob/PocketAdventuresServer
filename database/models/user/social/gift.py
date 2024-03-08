from database.database import db


# Gift are supposed to expire after 20 days
class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sku = db.Column(db.Integer, nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    sender_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Gift {}, {}>'.format(self.id, self.sku)
