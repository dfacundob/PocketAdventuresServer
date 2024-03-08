from command.base_command import BaseCommand

from database.models.galaxy.planet.bunkers.bunker_ship import BunkerShip


class DeployPoolUnitsOnBunkerHandler(BaseCommand):

    def process(self):
        bunker = self.user.profile.current_planet.bunkers.filter_by(sid=self.command_data['bunkerSid']).first()

        if bunker is not None:
            for units in self.command_data['unitsArray']:
                ship = self.user.profile.alliance_ships.filter_by(sku=units['sku'], expire_at=units['time']).first()

                if ship is not None:
                    ship.amount -= units['amount']

                    if ship.amount <= 0:
                        ship.delete()

                    for _ in range(units['amount']):
                        bunker.bunker_ships.append(BunkerShip(
                            sku=ship.sku
                        ))

                    self.user.profile.save()

                else:
                    print('An user tried to deploy unknown alliance units in a bunker: {}'.format(self.user.profile.id))

        else:
            print('An user tried to deploy alliance units in an unknown bunker: {}'.format(self.user.profile.id))
