import json

from datetime import datetime, timedelta

from database.database import db
from utils.utils import npc_bases


class Npcs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)

    last_attacked = db.Column(db.String(100), nullable=False, default='')

    firebit_progress = db.Column(db.Integer, nullable=False, default=1)
    reptice_progress = db.Column(db.Integer, nullable=False, default=1)
    elderby_progress = db.Column(db.Integer, nullable=False, default=1)
    sparragon_progress = db.Column(db.Integer, nullable=False, default=1)

    last_firebit_attack_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_reptice_attack_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_elderby_attack_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_sparragon_attack_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Thoses are the npc's base stored as json so we don't have to encode them back
    firebit_base = db.Column(db.Text, nullable=False, default=json.dumps(npc_bases['npc_B'][1]))
    reptice_base = db.Column(db.Text, nullable=False, default=json.dumps(npc_bases['npc_D'][1]))
    elderby_base = db.Column(db.Text, nullable=False, default=json.dumps(npc_bases['npc_A'][1]))
    sparragon_base = db.Column(db.Text, nullable=False, default=json.dumps(npc_bases['npc_C'][1]))

    def get_npc_progress(self, npc_sku):
        if npc_sku == 'npc_A':
            return self.elderby_progress

        elif npc_sku == 'npc_B':
            return self.firebit_progress

        elif npc_sku == 'npc_C':
            return self.sparragon_progress

        else:
            return self.reptice_progress

    def increment_npc_progress(self):
        if len(npc_bases[self.last_attacked]) > self.get_npc_progress(self.last_attacked):
            if self.last_attacked == 'npc_A':
                self.elderby_progress += 1

            elif self.last_attacked == 'npc_B':
                self.firebit_progress += 1

            elif self.last_attacked == 'npc_C':
                self.sparragon_progress += 1

            else:
                self.reptice_progress += 1

            # update the npc base
            self.set_npc_base(self.last_attacked, npc_bases[self.last_attacked][self.get_npc_progress(self.last_attacked)])

    def get_last_attack_date(self, npc_sku):
        if npc_sku == 'npc_A':
            return self.last_elderby_attack_date

        elif npc_sku == 'npc_B':
            return self.last_firebit_attack_date

        elif npc_sku == 'npc_C':
            return self.last_sparragon_attack_date

        else:
            return self.last_reptice_attack_date

    def update_last_attack_date(self, npc_sku):
        if npc_sku == 'npc_A':
            self.last_elderby_attack_date = datetime.utcnow()

        elif npc_sku == 'npc_B':
            self.last_firebit_attack_date = datetime.utcnow()

        elif npc_sku == 'npc_C':
            self.last_sparragon_attack_date = datetime.utcnow()

        else:
            self.last_reptice_attack_date = datetime.utcnow()

    def get_npc_base(self, npc_sku):
        if npc_sku in npc_bases:
            last_attack_date = self.get_last_attack_date(npc_sku)

            if datetime.utcnow() - last_attack_date >= timedelta(hours=6):
                npc_progress = self.get_npc_progress(npc_sku)
                self.set_npc_base(npc_sku, npc_bases[npc_sku][npc_progress])

            if npc_sku == 'npc_A':
                return json.loads(self.elderby_base)

            elif npc_sku == 'npc_B':
                return json.loads(self.firebit_base)

            elif npc_sku == 'npc_C':
                return json.loads(self.sparragon_base)

            else:
                return json.loads(self.reptice_base)

        else:
            return None

    def set_npc_base(self, npc_sku, npc_base):
        if npc_sku == 'npc_A':
            self.elderby_base = json.dumps(npc_base)

        elif npc_sku == 'npc_B':
            self.firebit_base = json.dumps(npc_base)

        elif npc_sku == 'npc_C':
            self.sparragon_base = json.dumps(npc_base)

        else:
            self.reptice_base = json.dumps(npc_base)

        self.save()

    @property
    def attacked_npc_base(self):
        return self.get_npc_base(self.last_attacked)

    def __repr__(self):
        return '<Npcs {}>'.format(self.id)
