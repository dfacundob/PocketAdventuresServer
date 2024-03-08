from command.base_command import BaseCommand

from database.models.user.profile import UserProfile


class GetMyAllianceHandler(BaseCommand):

    def answer(self):
        # Called getMyAlliance but can be used to request other players alliance, ubisoft is clowning me

        if self.command_data['guid'] == self.user.profile.id:
            profile = self.user.profile

        else:
            profile = UserProfile.query.get(self.command_data['guid'])

        if profile is not None:
            if profile.has_alliance:
                include_members = self.command_data['includeMembers'] == 'true'

                self.answer_command_data['alliance'] = profile.Alliance.encode(encode_members=include_members)

                if profile.id == self.user.profile.id:
                    self.answer_command_data['alliance']['items'] = []

                    for powerup_sku in self.command_data['items']:
                        power_up = profile.Alliance.power_ups.filter_by(sku=powerup_sku).first()

                        if power_up is not None:
                            self.answer_command_data['alliance']['items'].append(power_up.encode())

                        else:
                            print('An user tried to get an unknown alliance powerup info, sku: {}'.format(powerup_sku))

                    profile.Alliance.refresh_war_info()

        else:
            print('An user tried to query the alliance of an unknow profile: {}'.format(self.command_data['guid']))
