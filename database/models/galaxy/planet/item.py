from datetime import datetime
from database.database import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    upgrade_id = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    is_flipped = db.Column(db.Integer, nullable=False)
    repairing = db.Column(db.Integer, nullable=False)
    income_to_restore = db.Column(db.Integer, nullable=False)
    energy = db.Column(db.Integer, nullable=False)

    @property
    def calculate_energy(self):
        return not self.sku.startswith(('o_001', 'd_001'))  # everything except obstacles & decorations

    @property
    def time(self):
        return max(0, int((self.end_time - datetime.utcnow()).total_seconds() * 1000))

    def __repr__(self):
        return '<Item {}, {}>'.format(self.id, self.sku)
