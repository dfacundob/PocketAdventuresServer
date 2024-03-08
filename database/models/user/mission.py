from database.database import db


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.String(100), nullable=False)

    def get_progress(self):
        return list(map(int, self.progress.split(',')))

    def set_progress(self, progress):
        self.progress = ','.join(map(str, progress))

    def __repr__(self):
        return '<Mission {}, {}>'.format(self.id, self.sku)
