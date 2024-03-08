from command.base_command import BaseCommand

from database.models.user.social.gift import Gift
from database.models.user.profile import UserProfile


class SendGiftHandler(BaseCommand):

    def answer(self):
        request_id = self.command_data['requestId']

        if self.user.profile.can_send_gift(self.command_data['sku']):
            if request_id:
                # Means we send a gift back (should never happen since we disabled sendback in get-incoming-gift)
                gift = Gift.query.get(request_id)

                if gift is not None:
                    gift.delete()

            for user_id in self.command_data['targetIds']:
                receiver = UserProfile.query.get(user_id)

                if receiver is not None:
                    receiver.gifts.append(Gift(
                        sku=self.command_data['sku'],
                        sender_id=self.user.profile.id
                    ))

                    self.user.profile.update_gift_timestamp(self.command_data['sku'])

                    self.user.profile.save()
                    receiver.save()

        else:
            self.answer_command_data['responses'] = []
            self.answer_command_data['responses'].append({'sent': False})
