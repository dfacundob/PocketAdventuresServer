from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance
from database.models.alliances.alliance_invite import AllianceInvite
from utils.enums import LOG_TYPE, ALLIANCE_ROLE


class LeaveAllianceHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            alliance = Alliance.query.get(self.command_data['aid'])

            if alliance is not None:
                alliance.members.remove(self.user.profile)

                alliance.add_log(
                    subtype=LOG_TYPE.USER_LEFT,
                    name=self.user.profile.username,
                    user_avatar=self.user.profile.user_avatar,
                    user_level=self.user.profile.level_based_on_score
                )

                if not alliance.members.count():
                    for alliance_invite in AllianceInvite.query.filter_by(alliance_id=self.command_data['aid']).all():
                        alliance_invite.delete()

                    alliance.delete()

                elif self.user.profile.role == 'LEADER':
                    new_leader = alliance.get_potential_new_leader()
                    new_leader.role = ALLIANCE_ROLE.LEADER

                    alliance.add_log(
                        subtype=LOG_TYPE.LEADER_PROMOTION,
                        name=new_leader.username,
                        user_avatar=new_leader.user_avatar,
                        user_level=new_leader.level_based_on_score
                    )

                for units in self.user.profile.alliance_ships:
                    units.delete()

                self.user.profile.save()

            else:
                print('An user tried to leave an unknown alliance: {}'.format(self.command_data['aid']))

        else:
            print('An user tried to leave an alliance that he doesn\'t belong to: {}'.format(self.user.profile.id))
