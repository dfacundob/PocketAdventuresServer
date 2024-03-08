from command.base_command import BaseCommand
from utils.enums import LOG_TYPE


class TagPlanetHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            self.user.profile.Alliance.add_log(
                subtype=LOG_TYPE.PLANET_TAGGED,
                name=self.user.profile.username,
                user_avatar=self.user.profile.user_avatar,
                user_level=self.user.profile.level_based_on_score,
                enemy_id=self.command_data['enemyId'],
                enemy_name=self.command_data['enemyName'],
                enemy_planet_id=self.command_data['planetId']
            )

            self.user.profile.Alliance.save()

        else:
            print('An user tried to tag a planet but doesn\'t belong to any alliance: {}'.format(self.user.profile))
