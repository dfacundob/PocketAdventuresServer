from command.base_command import BaseCommand


class UpdateMiscHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['action'] = 'storePushNotificationInfo'

        if self.command_data['action'] == 'firstLoadingSuccess':
            if self.command_data['chk'] != -2114504928:
                self.logout_player()
