from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance


class DenyAllianceRequestHandler(BaseCommand):

    def process(self):
        request_type = self.command_data['messageType']

        if request_type == 'join':
            if self.user.profile.has_alliance:
                alliance = Alliance.query.get(self.command_data['aid'])

                if alliance is not None:
                    request = alliance.requests.filter_by(user_id=self.command_data['senderId']).first()

                    if request is not None:
                        request.delete()

                    else:
                        print('An user tried to deny an unknown alliance request: {}'.format(self.command_data['senderId']))

                else:
                    print('An user tried to deny a request from an alliance that doesn\'t exist: {}'.format(self.command_data['aid']))

            else:
                print('An user tried to deny an alliance request but doesn\'t belong to any alliance: {}'.format(self.user.profile.id))

        else:
            alliance_invite = self.user.profile.incoming_alliance_invites.filter_by(sender_profile_id=self.command_data['senderId']).first()

            if alliance_invite is not None:
                alliance_invite.delete()

            else:
                print('An user tried to delete an unknown invite from: {}'.format(self.command_data['senderId']))
