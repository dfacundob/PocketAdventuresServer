from command.base_command import BaseCommand
from database.models.alliances.alliance_ship import AllianceShip


class QueryAllianceGiftUnitsOnPoolHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            target_user = self.user.profile.Alliance.members.filter_by(id=self.command_data['targetAccountId']).first()

            if target_user is not None:
                for units in self.command_data['unitsArray']:
                    hangar = self.user.profile.current_planet.hangars.filter_by(sid=units['hangarSid']).first()

                    if hangar is not None:
                        ships = hangar.hangar_ships.filter_by(sku=units['sku']).limit(units['amount']).all()

                        if ships is not None:
                            for ship in ships:
                                ship.delete()

                            target_user.alliance_ships.append(AllianceShip(
                                sku=units['sku'],
                                amount=units['amount']
                            ))

                            target_user.save()

                        else:
                            print('An user tried to gift unknown units: {}'.format(units['sku']))

                    else:
                        print('An user tried to send units to an alliance member from an unknown hangar: {}'.format(units['hangarSid']))

            else:
                print('An user tried to gift units to an unknown alliance member: {}'.format(self.command_data['targetAccountId']))

        else:
            print('An user tried to gift unit to an alliance member but doesn\'t belong to any alliance: {}'.format(self.user.profile.id))
