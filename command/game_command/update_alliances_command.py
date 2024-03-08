import json

from datetime import datetime
from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance
from utils.enums import ALLIANCE_ROLE
from utils.errors import ALLIANCE_ERROR


class UpdateAlliancesHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']

        self.answer_command_data['requestParams'] = {}
        self.answer_command_data['requestParams']['action'] = action

        if action == 'createAlliance':
            if not self.user.profile.has_alliance:
                name_taken = Alliance.query.filter_by(name=self.command_data['name']).first() is not None

                if not name_taken:
                    logo = ':'.join(map(str, self.command_data['logo']))

                    self.alliance = Alliance(name=self.command_data['name'],
                                             alliance_logo=logo).save()

                    self.user.profile.role = ALLIANCE_ROLE.LEADER
                    self.user.profile.joined_alliance_time = datetime.utcnow()
                    self.alliance.members.append(self.user.profile)

                    self.handle_transaction()
                    self.user.profile.save()

                    self.answer_command_data['responseJSON'] = json.dumps(self.alliance.encode())

                else:
                    self.answer_command_data['responseJSON'] = json.dumps({'error': ALLIANCE_ERROR.NAME_ALREADY_TAKEN})
