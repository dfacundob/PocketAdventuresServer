from database.database import db


class SocialItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    counter = db.Column(db.Integer, nullable=False, default=0)
    position = db.Column(db.Integer, nullable=False, default=1)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<SocialItem {}, {}>'.format(self.id, self.sku)
