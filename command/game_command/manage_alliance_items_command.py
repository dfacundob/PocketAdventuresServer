from command.base_command import BaseCommand


class ManageAllianceItemsHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            power_up = self.user.profile.Alliance.power_ups.filter_by(sku=self.command_data['sku']).first()

            if power_up is not None:
                action = self.command_data['action']

                if action == 'activate':
                    power_up.activate()

                elif action == 'contribute':
                    power_up.contribution += self.command_data['quantity']

            else:
                print('An user tried to manage an unknown alliance powerup: {}'.format(self.command_data['sku']))

        else:
            print('An user tried to manage alliance items but doesn\'t belong to an alliance: {}'.format(self.user.profile.id))
