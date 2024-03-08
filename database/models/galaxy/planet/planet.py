from datetime import datetime
from database.database import db
from utils.utils import items_energy


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    galaxy_id = db.Column(db.Integer, db.ForeignKey('galaxy.id'), nullable=False)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))

    planet_id = db.Column(db.Integer)
    position = db.Column(db.Integer, nullable=False)

    is_occupied = db.Column(db.Boolean, nullable=False, default=False)
    last_visited_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    droids = db.Column(db.Integer, nullable=False, default=1)
    hq_level = db.Column(db.Integer, default=1)
    coins_limit = db.Column(db.Integer, nullable=False, default=0)
    minerals_limit = db.Column(db.Integer, nullable=False, default=0)

    # Used to calculate damage percent for shield
    total_energy = db.Column(db.Integer, nullable=False, default=0)
    current_energy = db.Column(db.Integer, nullable=False, default=0)

    items = db.relationship('Item', backref='Planet', lazy='dynamic')
    hangars = db.relationship('Hangar', backref='Planet', lazy='dynamic')
    bunkers = db.relationship('Bunker', backref='Planet', lazy='dynamic')
    shipyards = db.relationship('Shipyard', backref='Planet', lazy='dynamic')
    game_units = db.relationship('GameUnit', backref='Planet', lazy='dynamic')

    def encode(self):
        planet_info = {}
        planet_info['Planet'] = []

        planet_info['sku'] = self.sku
        planet_info['planetId'] = self.planet_id
        planet_info['capital'] = self.capital
        planet_info['HQLevel'] = self.hq_level
        planet_info['starName'] = self.Galaxy.name
        planet_info['starId'] = self.Galaxy.id
        planet_info['starType'] = self.Galaxy.type
        planet_info['planetType'] = self.planet_type
        planet_info['coinsLimit'] = self.coins_limit
        planet_info['mineralsLimit'] = self.minerals_limit

        return planet_info

    def repair(self):
        for item in self.items:
            if item.calculate_energy:
                item.energy = items_energy[item.sku][str(item.upgrade_id)]

        self.save()

    @property
    def sku(self):
        return ':'.join(map(str, (
            self.Galaxy.x,
            self.Galaxy.y,
            self.position
        )))

    @property
    def capital(self):
        return self.planet_id == 1

    @property
    def planet_type(self):
        # Finally found this field utility, it's used to determine the planet background in replay mode
        if self.capital:
            return 1

        else:
            return self.Galaxy.type + 2

    @property
    def damage_percent(self):
        return ((self.total_energy - self.current_energy) / self.total_energy) * 100

    @property
    def last_visit_time(self):
        return int((datetime.utcnow() - self.last_visited_time).total_seconds() * 1000)

    @last_visit_time.setter
    def last_visit_time(self, value):
        self.last_visited_time = value

    def __repr__(self):
        return '<Planet {}, {}>'.format(self.id, self.sku)
