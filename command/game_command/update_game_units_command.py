from datetime import datetime, timedelta
from command.base_command import BaseCommand
from database.models.galaxy.planet.game_unit import GameUnit


class UpdateGameUnitsHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']
        planet = self.user.profile.current_planet

        if action == 'unlockStart':
            planet.game_units.append(GameUnit(
                sku=self.command_data['sku'],
                end_time=datetime.utcnow() + timedelta(milliseconds=self.command_data['timeLeft'])
            ))

        else:
            unit = planet.game_units.filter_by(sku=self.command_data['sku']).first()

            if unit is not None:
                if action == 'unlockCancel':
                    unit.delete()

                elif action == 'unlockCompleted':
                    unit.unlocked = True
                    unit.is_upgrading = False

                elif action == 'upgradeStart':
                    unit.is_upgrading = True
                    unit.end_time = datetime.utcnow() + timedelta(milliseconds=self.command_data['timeLeft'])

                elif action == 'upgradeCancel':
                    unit.is_upgrading = False

                elif action == 'upgradeCompleted':
                    unit.is_upgrading = False
                    unit.upgrade_id += 1

            else:
                print('{} on unknown game unit'.format(action))
                return False

        self.handle_transaction()
        self.user.profile.save()
