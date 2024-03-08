from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance


class GetAllianceHandler(BaseCommand):

    def answer(self):
        alliance = Alliance.query.get(self.command_data['aid'])

        include_members = self.command_data['includeMembers'] == 'true'

        if alliance is not None:
            self.answer_command_data['alliance'] = alliance.encode(encode_members=include_members)

        else:
            print('An unknown alliance got queried: {}'.format(self.command_data['aid']))
