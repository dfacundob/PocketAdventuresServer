from datetime import datetime

from command.base_command import BaseCommand
from database.models.alliances.alliance_ship import AllianceShip


class ObtainAllianceHelpsHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['AllianceHelpList'] = []

        if self.user.profile.has_alliance:
            game_units = {}
            game_units['GameUnits'] = []

            actual_time = int(datetime.utcnow().timestamp() * 1000)

            for ship in self.user.profile.alliance_ships.filter(AllianceShip.expire_at > actual_time):
                game_units['GameUnits'].append(ship.encode())

            self.answer_command_data['AllianceHelpList'].append(game_units)
