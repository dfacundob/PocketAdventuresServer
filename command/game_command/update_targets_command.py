from command.base_command import BaseCommand


class UpdateTargetsHandler(BaseCommand):

    def process(self):
        # as there's only one action possible we don't check the action field

        mission = self.user.profile.missions.filter_by(sku=self.command_data['sku']).first()

        if mission is not None:
            progress = mission.get_progress()
            sub_target_index = self.command_data['subTargetIndex']

            if len(progress) >= sub_target_index + 1:
                progress[sub_target_index] += self.command_data['amount']
                mission.set_progress(progress)

            else:
                print('An user tried to update target of a mission ({}) with an out of bound progress index: {}'.format(
                    self.command_data['sku'],
                    sub_target_index
                ))
                return False

        else:
            print('An user tried to update target of a mission he doesn\'t unlocked: {}'.format(self.command_data['sku']))
            return False

        self.user.profile.save()
