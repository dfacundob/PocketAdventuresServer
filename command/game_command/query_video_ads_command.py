from command.base_command import BaseCommand


class QueryVideoAdsHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['action'] = self.command_data['action']

        self.answer_command_data['timeLeft'] = 0
