from command.base_command import BaseCommand


class SetMessageOfTheDayHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            self.user.profile.Alliance.message_of_the_day = self.command_data['message']
            self.user.profile.Alliance.save()

        else:
            print('An user tried to set the message of the day in an alliance but doesn\'t belong to any alliance')
