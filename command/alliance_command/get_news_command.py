from command.base_command import BaseCommand
from database.models.alliances.alliance_log import AllianceLog


class GetNewsHandler(BaseCommand):
    def process(self):
        if self.user.profile.has_alliance:
            self.news = self.user.profile.Alliance.logs.order_by(AllianceLog.id.desc()) \
                                                       .limit(self.command_data['count'] % 31) \
                                                       .offset(self.command_data['fromIndex']).all()

        else:
            print('An user tried to getNews without having an alliance: {}'.format(self.user.profile.id))
            return False

    def answer(self):
        # Supposed to displayed stuff like who joined, who got promoted etc...
        # List of type:
        #   - 1: Alliance type ?
        #   - 2: pass
        # TID_ALLIANCE_POPUP_WARLOG_VOID (2, 3)

        # List of subtype:
        #   - 1: user joined
        #   - 2: user quit
        #   - 3: user kicked
        #   - 4: promoted leader
        #   - 5 & 13: promoted admin
        #   - 6 & 7: unused ?
        #   - 8 & 9: War started
        #   - 10: War won (params: warpointsWon)
        #   - 11: War lost (params: warpointsWon)
        #   - 12: Alliance created
        #   - 14: TID_ALLIANCES_ASK_FOR_HELP (not defined in locales)
        #   - 16: Planet tagged (params: enemyName and probably enemyId, planetId)
        #   - 17: War canceled

        self.answer_command_data['news'] = []

        for new in self.news:
            self.answer_command_data['news'].append(new.encode())
