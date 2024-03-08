from command.base_command import BaseCommand


class ObtainHangarsHelpHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['HangarsHelpList'] = []
