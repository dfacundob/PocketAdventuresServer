from database.database import db


class BattleEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('battle.id'), nullable=False)

    sku = db.Column(db.String(100), nullable=False)
    x = db.Column(db.Integer, nullable=True)
    y = db.Column(db.Integer, nullable=True)
    time = db.Column(db.Integer, nullable=False)

    def encode(self):
        battle_event_info = {}

        battle_event_info['sku'] = self.sku
        battle_event_info['time'] = self.time

        if self.x is not None:
            battle_event_info['x'] = self.x

        if self.y is not None:
            battle_event_info['y'] = self.y

        return battle_event_info

    def __repr__(self):
        return '<BattleEvent {}, {}>'.format(self.id, self.sku)
