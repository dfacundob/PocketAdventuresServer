from command.base_command import BaseCommand


class GetIncomingGiftsHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['info'] = []

        for gift in self.user.profile.gifts:
            gift_info = {}

            gift_info['requestId'] = gift.id
            gift_info['accepted'] = gift.accepted
            gift_info['accountId'] = gift.sender_id
            gift_info['giftSku'] = gift.sku
            gift_info['expired'] = False

            self.answer_command_data['info'].append(gift_info)
