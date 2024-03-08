from command.base_command import BaseCommand
from database.models.galaxy.galaxy import Galaxy


class QueryPlanetAvailabilityHandler(BaseCommand):

    def process(self):
        galaxy = Galaxy.query.get(self.command_data['starId'])

        self.answer_command_data['lockSuccess'] = 0

        if galaxy is not None:
            galaxy_x, galaxy_y, position = map(int, self.command_data['planetSku'].split(':'))
            planet = galaxy.planets.filter_by(position=position).first()

            if planet is not None:
                if not planet.is_occupied:
                    main_planet = self.user.profile.planets.filter_by(planet_id=1).first()
                    laboratory = main_planet.items.filter_by(sku='labs_observatory').first()

                    if laboratory is not None:
                        if not laboratory.upgrade_id >= len(self.user.profile.planets.all()) - 1:
                            print('An user tried to colonize a planet with too low level observatory !')
                            return False

                    else:
                        print('An user tried to colonize a planet without having a laboratory !')
                        return False

                else:
                    print('An user tried to colonize an already occupied planet: {} in galaxy {}-{}'.format(position, galaxy_x, galaxy_y))
                    return False

            else:
                print('An user tried to colonize an unknown planet: {} in galaxy {}-{}'.format(position, galaxy_x, galaxy_y))
                return False

        else:
            print('An user tried to colonize a planet in an unknown galaxy: {}'.format(self.command_data['starId']))
            return False

    def answer(self):
        self.answer_command_data['lockSuccess'] = 1
