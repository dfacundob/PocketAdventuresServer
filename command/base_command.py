# pylint: disable=unused-variable

from database.models.user.social_item import SocialItem


class BaseCommand:

    command_name = None

    def __init__(self, user, command_data, answer_command_data, answer_list=None):
        self.user = user
        self.command_data = command_data
        self.answer_command_data = answer_command_data
        self.answer_list = answer_list

    def process_command(self):
        if self.process() is None:
            self.answer()

    def process(self):
        pass

    def answer(self):
        pass

    def handle_transaction(self, transaction_object=None, target_user=None):
        if transaction_object is None:
            transaction = self.command_data.get('transaction')

        else:
            transaction = transaction_object

        if target_user is None:
            target_user = self.user.profile

        if transaction is not None:
            score, minerals, coins, chips = map(int, transaction['client'].split(':'))

            # Though i would only have to disable it on Flash but ubi clowns force me to disable it on PA aswell
            # (gotta disable it cuz the game sometimes use the ennemy ressources amounts in the client field)
            # if chips != self.user.profile.chips:
            #     return self.logout_player()

            # Avoid ressources overlapping
            new_coins_amount = target_user.coins + transaction['coins']

            if new_coins_amount > target_user.max_coins:
                target_user.coins = target_user.max_coins

            # Avoid negative ressources
            elif new_coins_amount < 0:
                self.logout_player()

            else:
                target_user.coins = new_coins_amount

            new_minerals_amount = target_user.minerals + transaction['minerals']

            if new_minerals_amount > target_user.max_minerals:
                target_user.minerals = target_user.max_minerals

            elif new_minerals_amount < 0:
                self.logout_player()

            else:
                target_user.minerals = new_minerals_amount

            new_cash_amount = target_user.chips + transaction['cash']

            if new_cash_amount >= 0:
                target_user.chips = new_cash_amount

            else:
                self.logout_player()

            target_user.xp += transaction['exp']
            target_user.score += transaction.get('score', 0)

            social_items = transaction.get('socialItems')

            if social_items is not None:
                for social_item in social_items:
                    item = target_user.social_items.filter_by(sku=social_item['sku']).first()

                    if item is None and social_item['amount'] < 0:
                        item = SocialItem(sku=social_item['sku'], quantity=0)
                        target_user.social_items.append(item)

                    if item is not None:
                        if self.command_data['action'] == 'buyItem':  # Ubisoft devs are dumb af
                            item.quantity += social_item['amount']

                        else:
                            item.quantity -= social_item['amount']

                    else:
                        print('An user tried to make a transaction with a social item he don\'t own !')

    def logout_player(self):
        self.user.rollback()

        answer_command = {}
        answer_command['cmdName'] = 'logOut'
        answer_command['cmdData'] = {}
        answer_command['cmdData']['type'] = 'ServerError'
        answer_command['cmdData']['text'] = ''

        self.answer_list.append(answer_command)
