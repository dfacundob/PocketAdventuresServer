import random

from datetime import datetime, timedelta

from database.database import db
from database.models.user.npcs import Npcs
from database.models.user.powerup import PowerUp
from database.models.galaxy.galaxy import Galaxy
from database.models.battle.battle import Battle
from database.models.galaxy.planet.item import Item
from database.models.galaxy.planet.planet import Planet
from database.models.galaxy.planet.game_unit import GameUnit
from database.models.galaxy.planet.hangars.hangar import Hangar
from utils.utils import (default_player_items, get_next_galaxy_coordinate,
                         generate_random_galaxy_name, get_initial_gifts_timestamps)
from utils.enums import ALLIANCE_ROLE, PLAY_MODE


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id'))

    friend_code = db.Column(db.String(12), nullable=False, default=lambda: str(random.randint(100000000000, 999999999999)))
    last_login_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable=False, default='Galaxy')
    user_avatar = db.Column(db.String(100), nullable=False, default='-1:-1:-1:-1')
    world_name = db.Column(db.String(100), nullable=False, default='AWorldName')
    is_account_locked = db.Column(db.Boolean, default=False, nullable=False)
    is_tutorial_completed = db.Column(db.Boolean, default=False, nullable=False)
    level_based_on_score = db.Column(db.Integer, default=1, nullable=False)
    last_level_notified = db.Column(db.Integer, nullable=False, default=1)
    xp = db.Column(db.Float, nullable=False, default=0.00)
    coins = db.Column(db.Integer, nullable=False, default=1942)
    minerals = db.Column(db.Integer, nullable=False, default=900)
    chips = db.Column(db.Integer, nullable=False, default=100000)
    score = db.Column(db.Integer, nullable=False, default=0)
    starbase_capacity = db.Column(db.Integer, nullable=False, default=9000)
    actual_planet_index = db.Column(db.Integer, nullable=False, default=0)
    protection_end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    asked_for_help = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lock_end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    play_mode = db.Column(db.Integer, nullable=False, default=PLAY_MODE.PLAYING)

    # attack stuff
    last_attack_player_id = db.Column(db.Integer, nullable=True)
    last_attack_planet_id = db.Column(db.Integer, nullable=True)

    # stats stuff
    total_coins_looted = db.Column(db.Integer, nullable=False, default=0)
    total_minerals_looted = db.Column(db.Integer, nullable=False, default=0)
    total_attacks_done = db.Column(db.Integer, nullable=False, default=0)
    total_attacks_received = db.Column(db.Integer, nullable=False, default=0)
    total_bases_destroyed = db.Column(db.Integer, nullable=False, default=0)
    total_bases_lost = db.Column(db.Integer, nullable=False, default=0)

    total_coins_storage = db.Column(db.Integer, nullable=False, default=0)
    total_minerals_storage = db.Column(db.Integer, nullable=False, default=0)

    gifts_timestamps = db.Column(db.String(100), nullable=False, default=get_initial_gifts_timestamps)

    alliance_role = db.Column(db.Integer, nullable=True)
    joined_alliance_time = db.Column(db.DateTime, nullable=True)

    # Social
    gifts = db.relationship('Gift', backref='UserProfile', lazy='dynamic')
    messages = db.relationship('Message', backref='UserProfile', lazy='dynamic')
    outgoing_neighbour_requests = db.relationship('NeighbourRequest', backref='SenderProfile', lazy='dynamic', foreign_keys='NeighbourRequest.sender_profile_id')
    incoming_neighbour_requests = db.relationship('NeighbourRequest', backref='ReceiverProfile', lazy='dynamic', foreign_keys='NeighbourRequest.receiver_profile_id')
    neighbours = db.relationship('Neighbour', backref='UserProfile', lazy='dynamic')
    muted_users = db.relationship('MutedUser', backref='UserProfile', lazy='dynamic')

    # Attack
    attacks_done = db.relationship('Battle', backref='AttackerProfile', lazy='dynamic', foreign_keys='Battle.attacker_profile_id')
    attacks_received = db.relationship('Battle', backref='ReceiverProfile', lazy='dynamic', foreign_keys='Battle.receiver_profile_id')

    # Alliance
    alliance_ships = db.relationship('AllianceShip', backref='UserProfile', lazy='dynamic')
    outgoing_alliance_invites = db.relationship('AllianceInvite', backref='SenderProfile', lazy='dynamic', foreign_keys='AllianceInvite.sender_profile_id')
    incoming_alliance_invites = db.relationship('AllianceInvite', backref='ReceiverProfile', lazy='dynamic', foreign_keys='AllianceInvite.receiver_profile_id')

    # Universe
    npcs = db.relationship('Npcs', backref='UserProfile', uselist=False)
    flags = db.relationship('Flag', backref='UserProfile', lazy='dynamic')
    planets = db.relationship('Planet', backref='UserProfile', lazy='dynamic')
    missions = db.relationship('Mission', backref='UserProfile', lazy='dynamic')
    power_ups = db.relationship('PowerUp', backref='UserProfile', lazy='dynamic')
    social_items = db.relationship('SocialItem', backref='UserProfile', lazy='dynamic')
    stars_bookmarks = db.relationship('StarsBookmarks', backref='UserProfile', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.npcs is None:
            self.npcs = Npcs()

        for powerup_sku in ['3', '4', '5']:
            self.power_ups.append(PowerUp(
                sku=powerup_sku
            ))

        if not self.planets.all():
            # Get a planet from the latest galaxy and populate it

            latest_galaxy = Galaxy.query.order_by(Galaxy.id.desc()).first()

            if latest_galaxy is not None:
                if latest_galaxy.planets_occupied >= 4:
                    # create 5 empty galaxy for colonization + another galaxy for this new player
                    for _ in range(5):
                        x, y = get_next_galaxy_coordinate(latest_galaxy.x, latest_galaxy.y)

                        galaxy = Galaxy(
                            x=x,
                            y=y,
                            name=generate_random_galaxy_name(),
                            type=random.randint(0, 5)
                        ).save()

                        latest_galaxy = galaxy

                    x, y = get_next_galaxy_coordinate(latest_galaxy.x, latest_galaxy.y)

                    galaxy = Galaxy(
                        x=x,
                        y=y,
                        name=generate_random_galaxy_name(),
                        type=random.randint(0, 5)
                    ).save()

                else:
                    galaxy = latest_galaxy

            else:
                # Create the first galaxy
                galaxy = Galaxy(
                    x=0,
                    y=0,
                    name=generate_random_galaxy_name(),
                    type=random.randint(0, 5)
                ).save()

            planet = random.choice(galaxy.planets.filter_by(is_occupied=False).all())

            for item_info in default_player_items:
                item = Item(
                    sku=item_info['sku'],
                    sid=item_info['sid'],
                    upgrade_id=item_info['upgradeId'],
                    end_time=datetime.utcnow() + timedelta(milliseconds=item_info['time']),
                    state=item_info['state'],
                    x=item_info['x'],
                    y=item_info['y'],
                    type=item_info['type'],
                    is_flipped=item_info['isFlipped'],
                    repairing=item_info['repairing'],
                    income_to_restore=item_info['incomeToRestore'],
                    energy=item_info['energy']
                )

                planet.items.append(item)

                if item.calculate_energy:
                    planet.total_energy += item_info['energy']
                    planet.current_energy += item_info['energy']

            planet.hangars.append(Hangar(
                sid=25
            ))

            # Marine are unlocked by default to avoid laboratory crash
            planet.game_units.append(GameUnit(
                sku='groundUnits_001_001',
                unlocked=True,
                is_upgrading=False
            ))

            planet.planet_id = 1
            planet.is_occupied = True

            galaxy.planets_occupied += 1

            self.planets.append(planet)

            print('Added an user to galaxy: {}, {}, planet index: {}'.format(galaxy.x, galaxy.y, planet.position))

        else:
            print('{} already has planets'.format(self))

    def can_send_gift(self, gift_sku):
        gifts_timestamps = list(map(float, self.gifts_timestamps.split(':')))
        gift_timestamp = gifts_timestamps[int(gift_sku) - 1]

        return datetime.utcnow() - datetime.fromtimestamp(gift_timestamp) > timedelta(days=1)

    def update_gift_timestamp(self, gift_sku):
        gifts_timestamps = list(map(float, self.gifts_timestamps.split(':')))
        gifts_timestamps[int(gift_sku) - 1] = datetime.utcnow().timestamp()

        self.gifts_timestamps = ':'.join(map(str, gifts_timestamps))

    def get_active_alliance_powerup(self):
        if self.has_alliance:
            return self.Alliance.get_active_powerup()

    def is_war_opponent(self, user):
        if self.has_alliance and user.has_alliance:
            if self.role != 'RECRUIT' and user.role != 'RECRUIT':
                if self.Alliance.is_at_war and user.Alliance.is_at_war:
                    if self.Alliance.enemy_alliance_id == user.Alliance.id:
                        return True

        return False

    @property
    def avatar(self):
        return list(map(int, self.user_avatar.split(':')))

    @avatar.setter
    def avatar(self, avatar_list):
        self.user_avatar = ':'.join(map(str, avatar_list))

    @property
    def current_planet(self):
        return self.planets.order_by(Planet.planet_id.asc())[self.actual_planet_index]

    @property
    def current_battle(self):
        return self.attacks_done.order_by(Battle.id.desc()).first()

    @property
    def attacked_planet(self):
        return Planet.query.get(self.last_attack_planet_id)

    @property
    def has_shield(self):
        return self.protection_end_time >= datetime.utcnow()

    @property
    def is_under_attack(self):
        return self.lock_end_time >= datetime.utcnow()

    @property
    def protection_time_left(self):
        return max(0, int((self.protection_end_time - datetime.utcnow()).total_seconds() * 1000))

    @property
    def asked_for_help_end_time(self):
        return int(self.asked_for_help.timestamp() * 1000)

    @property
    def has_alliance(self):
        return self.alliance_id is not None

    @property
    def max_coins(self):
        return self.total_coins_storage + 9000

    @property
    def max_minerals(self):
        return self.total_minerals_storage + 9000

    @property
    def role(self):
        if self.alliance_role == ALLIANCE_ROLE.LEADER:
            return 'LEADER'

        elif self.alliance_role == ALLIANCE_ROLE.ADMIN:
            return 'ADMIN'

        elif self.alliance_role == ALLIANCE_ROLE.REGULAR:
            return 'REGULAR'

        else:
            return 'RECRUIT'

    @role.setter
    def role(self, role):
        self.alliance_role = role

    def __repr__(self):
        return '<UserProfile {}, {}>'.format(self.id, self.username)
