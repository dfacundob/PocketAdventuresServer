from command.base_command import BaseCommand

from database.models.user.social_item import SocialItem


class AcceptGiftHandler(BaseCommand):

    def answer(self):
        gift = self.user.profile.gifts.filter_by(id=self.command_data['requestId']).first()

        if gift is not None:
            item = self.user.profile.social_items.filter_by(sku=gift.sku).first()

            if item is not None:
                item.quantity += 1

            else:
                # Gifts sequence start at position 0 and not at 1 like other items (no size before sequence)
                self.user.profile.social_items.append(SocialItem(sku=gift.sku, position=0, quantity=1))

            self.answer_command_data['requestId'] = gift.id
            self.answer_command_data['available'] = False  # Allow to send a gift back (we disable that for technical issues)
            self.answer_command_data['sku'] = gift.sku

            gift.delete()

            self.user.profile.save()

        else:
            self.answer_command_data['error'] = 1
            self.answer_command_data['info'] = {}
            self.answer_command_data['info']['requestId'] = self.command_data['requestId']
