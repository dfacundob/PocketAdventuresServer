from command.base_command import BaseCommand
from utils.enums import LOG_TYPE


class KickMemberHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            kicked_user = self.user.profile.Alliance.members.filter_by(id=self.command_data['memberId']).first()

            if kicked_user is not None:
                self.user.profile.Alliance.members.remove(kicked_user)

                self.user.profile.Alliance.add_log(
                    subtype=LOG_TYPE.USER_KICKED,
                    name=kicked_user.username,
                    user_avatar=kicked_user.user_avatar,
                    user_level=kicked_user.level_based_on_score
                )

                for units in kicked_user.alliance_ships:
                    units.delete()

                kicked_user.role = None

                kicked_user.save()

            else:
                print('An user tried to kick an unknown user from his alliance: {}'.format(self.command_data['memberId']))

        else:
            print('An user tried to kick someone from an alliance but doesn\t belong to any alliance: {}'.format(self.user.profile.id))
