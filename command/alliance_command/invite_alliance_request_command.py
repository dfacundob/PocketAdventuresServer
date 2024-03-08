from command.base_command import BaseCommand

from database.models.user.profile import UserProfile
from database.models.alliances.alliance_invite import AllianceInvite
from utils.enums import ALLIANCE_INVITE


class InviteAllianceRequestHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            receiver = UserProfile.query.get(self.command_data['invitedId'])

            if receiver is not None:
                AllianceInvite(
                    type=ALLIANCE_INVITE.INVITE,
                    alliance_id=self.user.profile.Alliance.id,
                    alliance_name=self.user.profile.Alliance.name,
                    sender_profile_id=self.user.profile.id,
                    receiver_profile_id=receiver.id
                ).save()

            else:
                print('An user tried to invite an unknown profile in his alliance: {}'.format(self.command_data['inviteId']))

        else:
            print('An user tried to invite someone in an alliance but doesn\'t belong to any alliance: {}'.format(
                self.user.profile.id))
