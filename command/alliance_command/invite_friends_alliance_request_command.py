from command.base_command import BaseCommand
from database.models.alliances.alliance_invite import AllianceInvite
from utils.enums import ALLIANCE_INVITE


class InviteFriendsAllianceRequestHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            for user_id in self.command_data['invitedIds']:
                friend_profile = self.user.profile.neighbours.filter_by(friend_id=user_id).first()

                if friend_profile is not None:
                    AllianceInvite(
                        type=ALLIANCE_INVITE.INVITE,
                        alliance_id=self.user.profile.Alliance.id,
                        alliance_name=self.user.profile.Alliance.name,
                        sender_profile_id=self.user.profile.id,
                        receiver_profile_id=friend_profile.friend_id
                    ).save()

                else:
                    print('An user tried to invite an unknown profile in his alliance: {}'.format(user_id))

        else:
            print('An user tried to invite someone in an alliance but doesn\'t belong to any alliance: {}'.format(
                self.user.profile.id))
