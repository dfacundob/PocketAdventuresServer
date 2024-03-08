from database.database import db


class StarsBookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    star_id = db.Column(db.Integer, nullable=False)
    star_name = db.Column(db.String(100), nullable=False)
    edited_name = db.Column(db.String(100), nullable=False)

    @property
    def sku(self):
        return ':'.join(map(str, (
            self.x,
            self.y
        )))

    def __repr__(self):
        return '<StarBookmark {}, {}>'.format(self.id, self.star_name)
