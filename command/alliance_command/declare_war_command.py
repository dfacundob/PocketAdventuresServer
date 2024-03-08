from datetime import datetime

from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance
from utils.enums import LOG_TYPE
from utils.errors import ALLIANCE_ERROR


class DeclareWarHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            alliance = Alliance.query.get(self.command_data['aid'])

            if alliance is not None:
                if not alliance.is_at_war:
                    war_start_date = datetime.utcnow()

                    self.user.profile.Alliance.is_war_declarator = True
                    self.user.profile.Alliance.current_war_damage = 0
                    self.user.profile.Alliance.enemy_alliance_id = alliance.id
                    self.user.profile.Alliance.war_start_date = war_start_date
                    self.user.profile.Alliance.shield_end_time = None

                    alliance.is_war_declarator = False
                    alliance.current_war_damage = 0
                    alliance.enemy_alliance_id = self.user.profile.Alliance.id
                    alliance.war_start_date = war_start_date
                    alliance.shield_end_time = None

                    self.user.profile.Alliance.add_log(
                        subtype=LOG_TYPE.WAR_STARTED,
                        name=alliance.name,
                        logo=alliance.alliance_logo
                    )

                    alliance.add_log(
                        subtype=LOG_TYPE.WAR_STARTED,
                        name=self.user.profile.Alliance.name,
                        logo=self.user.profile.Alliance.alliance_logo
                    )

                    self.user.profile.Alliance.save()

                else:
                    self.answer_command_data['error'] = ALLIANCE_ERROR.ALREADY_AT_WAR

            else:
                print('An user tried to declare war to an unknown alliance: {}'.format(self.command_data['aid']))

        else:
            print('An user tried to declare war but doesn\'t belong to any alliance')
