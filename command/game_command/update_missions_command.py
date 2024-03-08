from command.base_command import BaseCommand
from utils.utils import missions_targets_size
from database.models.user.mission import Mission


class UpdateMissionsHandler(BaseCommand):

    def process(self):
        # as there's only one action possible we don't check the action field
        state = self.command_data['state']

        if state == 1:
            # readyToStart
            mission = self.user.profile.missions.filter_by(sku=self.command_data['sku']).first()

            if mission is None:
                progress_size = missions_targets_size.get(self.command_data['sku'])

                if progress_size is not None:
                    self.user.profile.missions.append(Mission(
                        sku=self.command_data['sku'],
                        state=state,
                        progress=','.join(progress_size * ['0'])
                    ))

                else:
                    print('An user got a new missions with unknown sku: {}'.format(self.command_data['sku']))
                    return False

            else:
                print('An user got a duplicated mission: {}'.format(self.command_data['sku']))
                return False

        else:
            mission = self.user.profile.missions.filter_by(sku=self.command_data['sku']).first()

            if mission is not None:
                mission.state = state

            else:
                print('An user tried to change state of a mission he doesn\'t unlocked, sku: {}'.format(self.command_data['sku']))
                return False

        self.handle_transaction()
        self.user.profile.save()
