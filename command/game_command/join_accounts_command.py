from command.base_command import BaseCommand


class JoinAccountsHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['action'] = self.command_data['action']

        if self.command_data['action'] == 'generateCode':
            self.answer_command_data['code'] = '999999999999'

        elif self.command_data['action'] == 'confirmCode':
            # self.answer_command_data['success'] = 1
            self.answer_command_data['errorCode'] = 3
