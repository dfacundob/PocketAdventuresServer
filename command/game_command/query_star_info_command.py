from command.base_command import BaseCommand
from database.models.galaxy.galaxy import Galaxy


class QueryStarInfoHandler(BaseCommand):

    def process(self):
        self.galaxy = Galaxy.query.get(self.command_data['starId'])

        if self.galaxy is None:
            print('An user tried to query an unknown galaxy: {}, {}'.format(self.command_data['coordX'], self.command_data['coordY']))
            return False

    def answer(self):
        self.answer_command_data['name'] = self.galaxy.name
        self.answer_command_data['starId'] = self.galaxy.id
        self.answer_command_data['type'] = self.galaxy.type

        self.answer_command_data['spaceStarInfo'] = []

        for planet in self.galaxy.planets.filter_by(is_occupied=True).all():
            planet_data = {}

            planet_data['sku'] = planet.sku
            planet_data['HQLevel'] = planet.hq_level
            planet_data['accountId'] = planet.UserProfile.User.id
            planet_data['capital'] = planet.capital
            planet_data['damageProtectionTimeLeft'] = planet.UserProfile.protection_time_left
            planet_data['isOnline'] = planet.UserProfile.User.is_online
            planet_data['name'] = planet.UserProfile.username
            planet_data['planetId'] = planet.planet_id
            planet_data['tutorialCompleted'] = planet.UserProfile.is_tutorial_completed
            planet_data['type'] = planet.planet_type
            planet_data['xp'] = planet.UserProfile.xp
            planet_data['score'] = planet.UserProfile.score
            planet_data['avatar'] = planet.UserProfile.avatar

            self.answer_command_data['spaceStarInfo'].append(planet_data)
