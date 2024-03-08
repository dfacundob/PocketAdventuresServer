from sqlalchemy import and_
from command.base_command import BaseCommand
from database.models.galaxy.galaxy import Galaxy


class QueryGalaxyWindowHandler(BaseCommand):

    def process(self):
        self.galaxies = Galaxy.query.filter(and_(Galaxy.x.between(self.command_data['topLeftCoordX'], self.command_data['bottomRightCoordX']),
                                                 Galaxy.y.between(self.command_data['topLeftCoordY'], self.command_data['bottomRightCoordY']))).all()

    def answer(self):
        self.answer_command_data['galaxyWindow'] = []

        for galaxy in self.galaxies:
            galaxy_info = {}
            galaxy_info['SpaceStar'] = ''
            galaxy_info['planetsFree'] = 8 - galaxy.planets_occupied
            galaxy_info['name'] = galaxy.name
            galaxy_info['type'] = galaxy.type
            galaxy_info['starId'] = galaxy.id
            galaxy_info['sku'] = galaxy.sku
            galaxy_info['planetsOccupied'] = galaxy.planets_occupied

            self.answer_command_data['galaxyWindow'].append(galaxy_info)
