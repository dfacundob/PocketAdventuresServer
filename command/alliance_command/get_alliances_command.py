from sqlalchemy import or_

from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance


class GetAlliancesHandler(BaseCommand):

    def process(self):
        search_key = self.command_data.get('searchKey')

        if search_key:
            self.alliances = Alliance.query.filter(or_(Alliance.name.like('{}%'.format(search_key)), Alliance.name.like('% {}%'.format(search_key)))) \
                                           .order_by(Alliance.warpoints.desc(), Alliance.created_at.asc()) \
                                           .limit(self.command_data['count'] % 51) \
                                           .offset(self.command_data['from']).all()

        else:
            self.alliances = Alliance.query.order_by(Alliance.warpoints.desc(), Alliance.created_at.asc()) \
                                           .limit(self.command_data['count'] % 51) \
                                           .offset(self.command_data['from']).all()

        self.answer_command_data['alliances'] = []

        if len(self.alliances) > 0:
            for index, alliance in enumerate(self.alliances):
                if search_key:
                    self.answer_command_data['alliances'].append(
                        alliance.encode(encode_members=False))

                else:
                    self.answer_command_data['alliances'].append(alliance.encode(
                        alliance_rank=self.command_data['from'] + index + 1, encode_members=False))  # Avoid calculating rank for each alliances

            self.answer_command_data['startIndex'] = self.command_data['from']
            self.answer_command_data['totalSize'] = self.command_data['from'] + len(
                self.alliances)

        else:
            # Basically prevent the game from bitching and literally sending 15 requests per seconds
            self.answer_command_data['response_code'] = 1
