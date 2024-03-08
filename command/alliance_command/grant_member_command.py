from command.base_command import BaseCommand
from utils.enums import ALLIANCE_ROLE, LOG_TYPE


class GrantMemberHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            user = self.user.profile.Alliance.members.filter_by(id=self.command_data['memberId']).first()

            if user is not None:
                role = self.command_data['role']

                if role == 'regular':
                    role = ALLIANCE_ROLE.REGULAR

                else:
                    role = ALLIANCE_ROLE.ADMIN  # Since you can't downgrade to recruit neither grant to leader

                    self.user.profile.Alliance.add_log(
                        subtype=LOG_TYPE.ADMIN_PROMOTION,
                        name=user.username,
                        user_avatar=user.user_avatar,
                        user_level=user.level_based_on_score
                    )

                user.role = role
                user.save()

            else:
                print('An user tried to grant an unknown user: {}'.format(self.command_data['memberId']))

        else:
            print('An user tried to grant an alliance member but doesn\t belong to any alliance: {}'.format(self.user.profile.id))
