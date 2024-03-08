from database.database import db


class AllianceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alliance_id = db.Column(db.Integer, db.ForeignKey('alliance.id', ondelete='CASCADE'), nullable=False)

    type = db.Column(db.Integer, nullable=False, default=1)
    subtype = db.Column(db.Integer, nullable=False)

    # Optional
    name = db.Column(db.String(100), nullable=True)
    logo = db.Column(db.String(100), nullable=True)
    user_level = db.Column(db.Integer, nullable=True)
    user_avatar = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)

    # Parameters
    enemy_id = db.Column(db.Integer, nullable=True)
    enemy_name = db.Column(db.String(100), nullable=True)
    enemy_planet_id = db.Column(db.Integer, nullable=True)
    warpoints_won = db.Column(db.Integer, nullable=True)

    def encode(self):
        log_info = {}

        log_info['id'] = self.id
        log_info['type'] = self.type
        log_info['subType'] = self.subtype
        log_info['raw'] = {}

        if self.logo is not None:
            log_info['logo'] = list(map(int, self.logo.split(':')))

        else:
            log_info['logo'] = self.Alliance.logo

        if self.timestamp is not None:
            log_info['timestamp'] = int(self.timestamp.timestamp() * 1000)

        if self.name is not None:
            log_info['name'] = self.name

        if self.user_level is not None:
            log_info['level'] = self.user_level

        if self.user_avatar is not None:
            log_info['avatar'] = list(map(int, self.user_avatar.split(':')))

        if self.enemy_id is not None:
            log_info['raw']['enemyId'] = self.enemy_id

        if self.enemy_name is not None:
            log_info['raw']['enemyName'] = self.enemy_name

        if self.enemy_planet_id is not None:
            log_info['raw']['planetId'] = self.enemy_planet_id

        if self.warpoints_won is not None:
            log_info['raw']['warpointsWon'] = self.warpoints_won

        return log_info

    def __repr__(self):
        return '<AllianceLog {}, {}>'.format(self.id, self.alliance_id)
