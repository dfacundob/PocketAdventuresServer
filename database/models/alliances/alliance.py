from datetime import datetime, timedelta
from sqlalchemy import or_, and_

from database.database import db
from database.models.user.profile import UserProfile
from database.models.alliances.alliance_log import AllianceLog
from database.models.alliances.alliance_request import AllianceRequest
from database.models.alliances.alliance_powerup import AlliancePowerUp

from utils.enums import LOG_TYPE, ALLIANCE_ROLE


class Alliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    name = db.Column(db.String(100), nullable=False)
    alliance_logo = db.Column(db.String(100), nullable=False)

    # Wars stuff
    last_war_info_refresh = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    warpoints = db.Column(db.Integer, nullable=False, default=0)
    wars_won = db.Column(db.Integer, nullable=False, default=0)
    wars_lost = db.Column(db.Integer, nullable=False, default=0)
    current_war_damage = db.Column(db.BigInteger, nullable=False, default=-1)
    enemy_alliance_id = db.Column(db.Integer, nullable=True)
    war_start_date = db.Column(db.DateTime, nullable=True)
    shield_end_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_war_declarator = db.Column(db.Boolean, nullable=True)

    motd = db.Column(db.String(200), nullable=True)
    motd_last_update = db.Column(db.DateTime, nullable=True)

    members = db.relationship('UserProfile', backref='Alliance', lazy='dynamic')
    requests = db.relationship('AllianceRequest', backref='Alliance', lazy='dynamic', cascade='all, delete-orphan')
    power_ups = db.relationship('AlliancePowerUp', backref='Alliance', lazy='dynamic', cascade='all, delete-orphan')
    logs = db.relationship('AllianceLog', backref='Alliance', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logs.append(AllianceLog(
            type=0,
            subtype=LOG_TYPE.ALLIANCE_CREATED,
            name=self.name
        ))

        for powerup_sku in ['1', '2', '5']:
            self.power_ups.append(AlliancePowerUp(
                sku=powerup_sku
            ))

    def encode(self, alliance_rank=None, encode_members=True):
        alliance_data = {}

        alliance_data['id'] = self.id
        alliance_data['name'] = self.name
        alliance_data['logo'] = self.logo
        alliance_data['messageOfTheDay'] = self.message_of_the_day

        if self.motd_last_update is not None:
            alliance_data['motdUpdatedAt'] = int(self.motd_last_update.timestamp() * 1000)

        if alliance_rank is not None:
            alliance_data['rank'] = alliance_rank

        else:
            alliance_data['rank'] = self.rank

        alliance_data['warsLost'] = self.wars_lost
        alliance_data['warsWon'] = self.wars_won
        alliance_data['totalWarScore'] = self.warpoints
        alliance_data['totalMembers'] = self.members.count()

        alliance_data['currentWarDamage'] = self.current_war_damage
        alliance_data['enemyAllianceId'] = self.enemy_alliance_id

        if self.war_start_date is not None:
            alliance_data['warStartTime'] = int(self.war_start_date.timestamp() * 1000)
            alliance_data['warEndTime'] = int((self.war_start_date + timedelta(days=7)).timestamp() * 1000)

        else:
            alliance_data['warStartTime'] = -1
            alliance_data['warEndTime'] = -1

        alliance_data['postWarShield'] = self.post_war_shield

        if encode_members:
            alliance_data['members'] = []

            for member in self.members.order_by(UserProfile.joined_alliance_time.asc()).all():
                member_data = {}

                member_data['id'] = member.id
                member_data['name'] = member.username
                member_data['planets'] = member.planets.count()
                member_data['role'] = member.role
                member_data['score'] = member.score

                # Seems unused
                # member_data['totalWarScore'] = 20
                # member_data['currentWarScore'] = 10

                member_data['askedForHelp'] = member.asked_for_help_end_time
                member_data['avatar'] = member.avatar

                alliance_data['members'].append(member_data)

        return alliance_data

    def refresh_war_info(self):
        # Refresh if more than one minute has passed since the last refresh
        if datetime.utcnow() >= self.last_war_info_refresh + timedelta(minutes=1):
            self.last_war_info_refresh = datetime.utcnow()

            if self.enemy_alliance_id is not None:
                ennemy_alliance = Alliance.query.get(self.enemy_alliance_id)

                ennemy_alliance.last_war_info_refresh = datetime.utcnow()
                ennemy_alliance.save()

                if datetime.utcnow() > self.war_start_date + timedelta(days=1):
                    if self.current_war_damage == 0 or ennemy_alliance.current_war_damage == 0:
                        self.set_post_war_info()
                        ennemy_alliance.set_post_war_info()

                        self.add_log(
                            subtype=LOG_TYPE.WAR_CANCELED,
                            timestamp=datetime.utcnow()
                        )

                        ennemy_alliance.add_log(
                            subtype=LOG_TYPE.WAR_CANCELED,
                            timestamp=datetime.utcnow()
                        )

                    elif datetime.utcnow() > self.war_start_date + timedelta(days=7):  # Means the war finished
                        if self.current_war_damage > ennemy_alliance.current_war_damage:
                            winner_alliance = self
                            loser_alliance = ennemy_alliance

                        elif self.current_war_damage < ennemy_alliance.current_war_damage:
                            winner_alliance = ennemy_alliance
                            loser_alliance = self

                        else:
                            if self.is_war_declarator:
                                winner_alliance = ennemy_alliance
                                loser_alliance = self

                            else:
                                winner_alliance = self
                                loser_alliance = ennemy_alliance

                        if winner_alliance.is_war_declarator:
                            # Scale factor based on war difficulty
                            win_factor = 2 + \
                                (loser_alliance.warpoints -
                                 winner_alliance.warpoints + 50) * 0.02

                        else:
                            win_factor = 2

                        winner_warpoints_won = int(win_factor * 70 * (winner_alliance.current_war_damage /
                                                                      (winner_alliance.current_war_damage + loser_alliance.current_war_damage)))
                        loser_warpoints_won = int(
                            70 * (loser_alliance.current_war_damage / (winner_alliance.current_war_damage + loser_alliance.current_war_damage)))

                        shield_end_time = self.war_start_date + timedelta(days=8)

                        winner_alliance.wars_won += 1
                        winner_alliance.warpoints += winner_warpoints_won
                        winner_alliance.add_log(
                            subtype=LOG_TYPE.WAR_WON,
                            name=loser_alliance.name,
                            warpoints_won=winner_warpoints_won
                        )
                        winner_alliance.set_post_war_info()

                        loser_alliance.wars_lost += 1
                        loser_alliance.warpoints += loser_warpoints_won
                        loser_alliance.add_log(
                            subtype=LOG_TYPE.WAR_LOST,
                            name=winner_alliance.name,
                            warpoints_won=loser_warpoints_won
                        )
                        loser_alliance.set_post_war_info()

                        winner_alliance.shield_end_time = shield_end_time
                        loser_alliance.shield_end_time = shield_end_time

            self.save()

    def set_post_war_info(self):
        self.is_war_declarator = None
        self.enemy_alliance_id = None
        self.war_start_date = None
        self.shield_end_time = None
        self.current_war_damage = -1

        for member in self.members:
            if member.role == 'RECRUIT':
                member.role = ALLIANCE_ROLE.REGULAR

    def add_log(self, **kwargs):
        self.logs.append(AllianceLog(**kwargs))

    def get_active_powerup(self):
        active_powerup = self.power_ups.filter(
            AlliancePowerUp.activation_time_end >= datetime.utcnow()).first()

        if active_powerup is not None:
            if active_powerup.sku == '1':
                return 'powerUp:6'

            elif active_powerup.sku == '2':
                return 'specialAttack:4'

            else:
                return 'powerUp:7'

    def get_potential_new_leader(self):
        # According to the server sources the first found admin is promoted to LEADER
        # if no admin are found we take the first soldier, if no soldier then the first recruit is promoted

        role_priority = [ALLIANCE_ROLE.ADMIN, ALLIANCE_ROLE.REGULAR, ALLIANCE_ROLE.RECRUIT]

        for role in role_priority:
            potential_new_leader = self.members.filter_by(alliance_role=role) \
                                               .order_by(UserProfile.joined_alliance_time.asc()).first()

            if potential_new_leader is not None:
                return potential_new_leader

    @property
    def logo(self):
        return list(map(int, self.alliance_logo.split(':')))

    @property
    def rank(self):
        return Alliance.query.filter(or_(Alliance.warpoints > self.warpoints,
                                         and_(Alliance.warpoints == self.warpoints,
                                              Alliance.created_at < self.created_at)
                                         )
                                     ).count() + 1

    @logo.setter
    def logo(self, logo_list):
        self.alliance_logo = ':'.join(map(str, logo_list))

    @property
    def message_of_the_day(self):
        return self.motd

    @message_of_the_day.setter
    def message_of_the_day(self, message):
        self.motd = message
        self.motd_last_update = datetime.utcnow()

    @property
    def is_full(self):
        return self.members.count() >= 20

    @property
    def is_flooded(self):
        return self.requests.filter(AllianceRequest.sent_date >= datetime.utcnow() - timedelta(days=3)).count() >= 20

    @property
    def is_at_war(self):
        if self.war_start_date is not None:
            return datetime.utcnow() < self.war_start_date + timedelta(days=7)

        else:
            return False

    @property
    def post_war_shield(self):
        if self.shield_end_time is not None:
            return int(self.shield_end_time.timestamp() * 1000)

        else:
            return -1

    def __repr__(self):
        return '<Alliance {}, {}>'.format(self.id, self.name)
