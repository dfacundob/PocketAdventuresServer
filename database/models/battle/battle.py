import json

from datetime import datetime
from database.database import db


class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    attacker_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    receiver_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    attack_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    coins_taken = db.Column(db.Integer, nullable=False, default=0)
    minerals_taken = db.Column(db.Integer, nullable=False, default=0)

    attacker_planet_id = db.Column(db.Integer, nullable=False)
    receiver_planet_id = db.Column(db.Integer, nullable=False)

    attacker_planet_coordinates = db.Column(db.String(100), nullable=False)
    receiver_planet_coordinates = db.Column(db.String(100), nullable=False)

    # Thoses are "frozen" info about the attacker & defender profile when the attack happened
    # We store them as json text so we don't have to encode anything when sending the replay
    universe = db.Column(db.Text, nullable=False)
    attacker_power_ups = db.Column(db.Text, nullable=True)
    attacker_game_units = db.Column(db.Text, nullable=False, default='')

    events = db.relationship('BattleEvent', backref='Battle', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, attacker, receiver, target_planet, attacker_planet, universe):
        # We just need one planet in the profile info so the game know the right planet type to display

        universe['Universe'][0]['Profile'][0]['Planets'] = [target_planet.encode()]

        attacker_planet_coordinates = ','.join(map(str, (
            attacker_planet.Galaxy.x,
            attacker_planet.Galaxy.y
            )))

        receiver_planet_coordinates = ','.join(map(str, (
            target_planet.Galaxy.x,
            target_planet.Galaxy.y
            )))

        attacker_game_units_info = []

        for game_unit in attacker.current_planet.game_units:
            game_unit_info = {}

            game_unit_info['sku'] = game_unit.sku
            game_unit_info['upgradeId'] = game_unit.upgrade_id

            attacker_game_units_info.append(game_unit_info)

        # PowerUps handling: after a few research it seems like the game only handle alliance powerups in replay
        # That mean if the attacker have an heroic potion active it won't be shown in the battle replay :/

        active_powerup = attacker.get_active_alliance_powerup()

        super().__init__(
            attacker_profile_id=attacker.id,
            receiver_profile_id=receiver.id,
            attacker_planet_id=attacker_planet.planet_id,
            receiver_planet_id=target_planet.planet_id,
            attacker_planet_coordinates=attacker_planet_coordinates,
            receiver_planet_coordinates=receiver_planet_coordinates,
            universe=json.dumps(universe),
            attacker_power_ups=active_powerup,
            attacker_game_units=json.dumps(attacker_game_units_info)
        )

    def encode(self, attacker):
        if attacker:
            profile = self.ReceiverProfile

        else:
            profile = self.AttackerProfile

        attack_info = {}

        attack_info['accountId'] = profile.id
        attack_info['attackDate'] = self.date

        if attacker:
            attack_info['star'] = self.receiver_planet_coordinates
            attack_info['planetId'] = self.receiver_planet_id

        else:
            attack_info['star'] = self.attacker_planet_coordinates
            attack_info['planetId'] = self.attacker_planet_id

        attack_info['coinsTaken'] = self.coins_taken
        attack_info['mineralsTaken'] = self.minerals_taken
        attack_info['userName'] = profile.username
        attack_info['mine'] = attacker
        attack_info['avatar'] = profile.avatar

        return attack_info

    @property
    def date(self):
        return int(self.attack_date.timestamp() * 1000)

    def __repr__(self):
        return '<Battle {}, {}>'.format(self.id, self.attack_date)
