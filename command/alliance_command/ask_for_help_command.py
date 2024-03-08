from datetime import datetime, timedelta

from command.base_command import BaseCommand


class AskForHelpHandler(BaseCommand):

    def process(self):
        self.user.profile.asked_for_help = datetime.utcnow() + timedelta(days=1)
        self.user.profile.save()
