import json

from command.base_command import BaseCommand
from database.models.battle.battle import Battle


class ObtainBattleReplayHandler(BaseCommand):

    def answer(self):
        battle = self.user.profile.attacks_received.order_by(Battle.id.desc()).first()

        if battle is not None:
            self.answer_command_data['Battle'] = []

            self.answer_command_data['Battle'].append(json.loads(battle.universe))

            if battle.attacker_power_ups is not None:
                power_ups_info = {}
                power_ups_info['powerUps'] = battle.attacker_power_ups

                self.answer_command_data['Battle'].append(power_ups_info)

            deploys_info = {}
            deploys_info['Deploys'] = []

            for deploy in battle.events:
                deploys_info['Deploys'].append(deploy.encode())

            self.answer_command_data['Battle'].append(deploys_info)

            attacker_game_units_info = {}
            attacker_game_units_info['AttackerGameUnits'] = json.loads(battle.attacker_game_units)

            self.answer_command_data['Battle'].append(attacker_game_units_info)

        else:
            print('An user tried to obtain a battle replay but none were found: {}'.format(self.user.profile.id))
