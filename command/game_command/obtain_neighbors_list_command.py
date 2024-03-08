from command.base_command import BaseCommand

from database.models.user.profile import UserProfile


class ObtainNeighborsListHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['neighborList'] = []

        for neighbour in self.user.profile.neighbours:
            neighbour_profile = UserProfile.query.get(neighbour.friend_id)

            if neighbour_profile is not None:
                neighbour_info = {}
                neighbour_info['neighbor'] = []

                neighbour_info['accountId'] = neighbour_profile.id
                neighbour_info['extId'] = neighbour_profile.id
                neighbour_info['name'] = neighbour_profile.username
                neighbour_info['wishlist'] = ''
                neighbour_info['xp'] = neighbour_profile.xp
                neighbour_info['levelBasedOnScore'] = neighbour_profile.level_based_on_score
                neighbour_info['score'] = neighbour_profile.score
                neighbour_info['tutorialCompleted'] = neighbour_profile.is_tutorial_completed
                neighbour_info['damageProtectionTimeLeft'] = 0

                if neighbour_profile.has_alliance:
                    neighbour_info['allianceName'] = neighbour_profile.Alliance.name
                    neighbour_info['allianceLogo'] = neighbour_profile.Alliance.logo

                planets_info = {}
                planets_info['Planets'] = []

                for planet in neighbour_profile.planets:
                    planets_info['Planets'].append(planet.encode())

                neighbour_info['neighbor'].append(planets_info)
                self.answer_command_data['neighborList'].append(neighbour_info)
