from command.base_command import BaseCommand


class ObtainSocialItemsHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['ItemsList'] = []

        for item in self.user.profile.social_items:
            item_data = {}
            item_data['sku'] = item.sku
            item_data['counter'] = item.counter
            item_data['quantity'] = item.quantity
            item_data['position'] = item.position

            item_data['timeLeft'] = 0
            item_data['timeOver'] = 0

            self.answer_command_data['ItemsList'].append(item_data)
