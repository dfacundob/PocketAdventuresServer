from datetime import datetime, timedelta
from command.base_command import BaseCommand
from utils.utils import get_default_colony_items
from database.models.galaxy.galaxy import Galaxy
from database.models.galaxy.planet.item import Item
from database.models.galaxy.planet.game_unit import GameUnit


class QueryGetColonyConfirmPurchaseHandler(BaseCommand):

    def process(self):
        galaxy = Galaxy.query.get(self.command_data['starId'])

        self.answer_command_data['colonyPurchaseSuccess'] = 0

        if galaxy is not None:
            galaxy_x, galaxy_y, position = map(int, self.command_data['planetSku'].split(':'))
            planet = galaxy.planets.filter_by(position=position).first()

            if planet is not None:
                if not planet.is_occupied:
                    main_planet = self.user.profile.planets.filter_by(planet_id=1).first()
                    laboratory = main_planet.items.filter_by(sku='labs_observatory').first()

                    if laboratory is not None:
                        if laboratory.upgrade_id >= len(self.user.profile.planets.all()) - 1:
                            planet.is_occupied = True
                            planet.planet_id = len(self.user.profile.planets.all()) + 1
                            galaxy.planets_occupied += 1

                            for item_info in get_default_colony_items(galaxy.type):
                                item = Item(
                                    sku=item_info['sku'],
                                    sid=item_info['sid'],
                                    upgrade_id=item_info['upgradeId'],
                                    end_time=datetime.utcnow() + timedelta(milliseconds=item_info['time']),
                                    state=item_info['state'],
                                    x=item_info['x'],
                                    y=item_info['y'],
                                    type=item_info['type'],
                                    is_flipped=item_info['isFlipped'],
                                    repairing=item_info['repairing'],
                                    income_to_restore=item_info['incomeToRestore'],
                                    energy=item_info['energy']
                                )

                                planet.items.append(item)

                                if item.calculate_energy:
                                    planet.total_energy += item_info['energy']
                                    planet.current_energy += item_info['energy']

                            # Marine are unlocked by default to avoid laboratory crash
                            planet.game_units.append(GameUnit(
                                sku='groundUnits_001_001',
                                unlocked=True,
                                is_upgrading=False
                            ))

                            self.user.profile.planets.append(planet)

                            self.handle_transaction()
                            self.user.profile.save()

                        else:
                            print('An user tried to colonize a planet with too low level observatory !')
                            return False

                    else:
                        print('An user tried to colonize a planet without having a laboratory !')
                        return False

                else:
                    print('An user tried to colonize an already occuped planet: {} in galaxy {}-{}'.format(position, galaxy_x, galaxy_y))
                    return False

            else:
                print('An user tried to confirm colonization of an unknown planet: {} in galaxy {}-{}'.format(position, galaxy_x, galaxy_y))
                return False

        else:
            print('An user tried to confirm colonization of a planet in an unknown galaxy: {}'.format(self.command_data['starId']))
            return False

    def answer(self):
        self.answer_command_data['colonyPurchaseSuccess'] = 1
