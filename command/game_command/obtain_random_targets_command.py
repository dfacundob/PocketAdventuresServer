from datetime import datetime, timedelta

from sqlalchemy import func, and_
from command.base_command import BaseCommand
from utils.utils import minimum_level_attack
from database.models.user.user import User
from database.models.user.profile import UserProfile
from database.models.galaxy.planet.planet import Planet


class ObtainRandomTargetsHandler(BaseCommand):

    def process(self):
        if str(self.user.profile.level_based_on_score) in minimum_level_attack:
            minimum_level = minimum_level_attack[str(self.user.profile.level_based_on_score)]

            # TODO: reduce thoses query times since they often timeout according to sentry
            if self.command_data['colonies'] == 'false':
                self.planets = Planet.query.join(UserProfile, User) \
                                           .filter(and_(User.id != self.user.id,
                                                        datetime.utcnow() - timedelta(minutes=6) >= User.last_command_time,
                                                        UserProfile.protection_end_time < datetime.utcnow(),
                                                        Planet.planet_id == 1,
                                                        UserProfile.level_based_on_score >= minimum_level)) \
                                           .order_by(func.random()).limit(10).all()

            else:
                self.planets = Planet.query.join(UserProfile, User) \
                                           .filter(and_(User.id != self.user.id,
                                                        datetime.utcnow() - timedelta(minutes=6) >= User.last_command_time,
                                                        Planet.planet_id != 1,
                                                        UserProfile.protection_end_time < datetime.utcnow(),
                                                        UserProfile.level_based_on_score >= minimum_level)) \
                                           .order_by(func.random()).limit(10).all()

        else:
            print('An user tried to obtain random targets with an unknown level: {} !'.format(self.user.profile.level_based_on_score))
            return False

    def answer(self):
        self.answer_command_data['nonFriendsList'] = []

        # Called nonFriendList but according to server sources they doesn't check if the users are our friends

        if self.command_data['colonies'] == 'false':
            self.answer_command_data['type'] = 'mainPlanets'

        else:
            self.answer_command_data['type'] = 'colonies'

        for planet in self.planets:
            if planet.damage_percent < 75:
                planet_info = {}
                planet_info['hqLevel'] = planet.hq_level
                planet_info['accountId'] = planet.UserProfile.User.id
                planet_info['name'] = planet.UserProfile.username
                planet_info['planetId'] = planet.planet_id
                planet_info['score'] = planet.UserProfile.score
                planet_info['avatar'] = planet.UserProfile.avatar
                planet_info['sku'] = planet.sku

                self.answer_command_data['nonFriendsList'].append(planet_info)
