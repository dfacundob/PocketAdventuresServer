from datetime import datetime, timedelta

from command.base_command import BaseCommand
from database.models.battle.battle import Battle


class ObtainAttackerLogHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['attackLog'] = []

        attacks = {}

        # We encode a maximum of 32 battle so 16 each
        for attack in self.user.profile.attacks_done.filter(Battle.attack_date >= datetime.utcnow() - timedelta(days=16)).order_by(Battle.attack_date.desc()).limit(16).all():
            attacks[attack.attack_date] = attack.encode(attacker=True)

        for attack in self.user.profile.attacks_received.filter(Battle.attack_date >= datetime.utcnow() - timedelta(days=16)).order_by(Battle.attack_date.desc()).limit(16).all():
            attacks[attack.attack_date] = attack.encode(attacker=False)

        # Oldest attack get encoded first
        for sorted_date in sorted(attacks):
            attack = attacks[sorted_date]

            self.answer_command_data['attackLog'].append(attack)
