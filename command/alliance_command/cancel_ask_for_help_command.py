from datetime import datetime

from command.base_command import BaseCommand


class CancelAskForHelpHandler(BaseCommand):

    def process(self):
        self.user.profile.asked_for_help = datetime.utcnow()
        self.user.profile.save()
