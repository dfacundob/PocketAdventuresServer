from datetime import datetime
from sqlalchemy import func

from command.base_command import BaseCommand
from database.models.alliances.alliance import Alliance


class GetShuffledSuggestedAlliancesHandler(BaseCommand):

    command_name = 'shuffleSuggestedAlliances'

    def answer(self):
        if self.user.profile.has_alliance:
            self.answer_command_data['alliances'] = []

            alliances = []

            # Hard alliance get encoded first, then intermediate then easy
            # For hard alliance we select alliances that have between our warpoints and 50 warpoints more than us
            # Medium alliance: between 25 warpoints less than us and 25 above us
            # Easy alliance: between 50 warpoints less than us and our warpoints
            alliance_difficulty = [0, -25, -50]

            for difficulty in alliance_difficulty:
                ennemy_alliance = Alliance.query.filter(
                    Alliance.id != self.user.profile.Alliance.id,
                    Alliance.shield_end_time < datetime.utcnow(),
                    Alliance.warpoints.between(
                        self.user.profile.Alliance.warpoints + difficulty,
                        self.user.profile.Alliance.warpoints + difficulty + 50
                        )
                ).order_by(func.random()).limit(1).first()

                if ennemy_alliance is not None:
                    alliances.append(ennemy_alliance.encode())

            if alliances:
                self.answer_command_data['alliances'].append(alliances)

        else:
            print('An user tried to query alliances for war but doesn\'t belong to any alliance')
