from datetime import datetime, timedelta

from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance
from database.models.alliances.alliance_request import AllianceRequest
from utils.errors import ALLIANCE_ERROR


class JoinAllianceHandler(BaseCommand):

    def process(self):
        if not self.user.profile.has_alliance:
            alliance = Alliance.query.get(self.command_data['aid'])

            if alliance is not None:
                already_sent = alliance.requests.filter(AllianceRequest.user_id == self.user.profile.id,
                                                        AllianceRequest.sent_date >= datetime.utcnow() - timedelta(days=3)) \
                                                .first() is not None

                if not already_sent:
                    if not alliance.is_flooded:
                        alliance.requests.append(AllianceRequest(
                            user_id=self.user.profile.id
                        ))

                        alliance.save()

                    else:
                        self.answer_command_data['error'] = ALLIANCE_ERROR.ALLIANCE_IS_FLOODED

                else:
                    self.answer_command_data['error'] = ALLIANCE_ERROR.REQUEST_ALREADY_SENT

            else:
                print('An usier tried to join an unknown alliance: {}'.format(self.command_data['aid']))

        else:
            print('An user tried to join an alliance but already belong to one: {}'.format(self.user.profile.id))
