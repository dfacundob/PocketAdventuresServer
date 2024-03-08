from command.base_command import BaseCommand


class RejectPoolUnitsHandler(BaseCommand):

    def process(self):
        for units in self.command_data['unitsArray']:
            ship = self.user.profile.alliance_ships.filter_by(
                sku=units['sku'],
                amount=units['amount'],
                expire_at=units['time']
            ).first()

            if ship is not None:
                ship.delete()

            else:
                print('An user tried to reject an unknown alliance help: {}'.format(self.user.profile.id))
