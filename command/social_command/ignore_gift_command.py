from command.base_command import BaseCommand


class IgnoreGiftHandler(BaseCommand):

    def answer(self):
        gift = self.user.profile.gifts.filter_by(id=self.command_data['requestId']).first()

        if gift is not None:
            gift.delete()

        else:
            print('An user tried to ignore a gift he never received: {}'.format(self.command_data['requestId']))
