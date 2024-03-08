from datetime import datetime, timedelta

from command.base_command import BaseCommand
from database.models.user.powerup import PowerUp
from database.models.user.social_item import SocialItem
from utils.utils import social_items, crafting_rewards, use_action_reward


class UpdateSocialItemHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']

        if action == 'nextStep':
            item = self.user.profile.social_items.filter_by(sku=self.command_data['sku']).first()

            if item is None:  # Means we have a new item
                item = SocialItem(
                    sku=self.command_data['sku'],
                    counter=self.command_data['currentCount'],
                    position=self.command_data['postion'],
                    quantity=self.command_data['currentQuantity']
                )

                self.user.profile.social_items.append(item)

            if item.sku in social_items:
                if len(social_items[item.sku]['sequence']) >= self.command_data['postion']:
                    if item.counter == social_items[item.sku]['size'] - 1:
                        item.position = 1

                    item.counter = self.command_data['currentCount']

                    if self.command_data['currentCount'] == social_items[item.sku]['sequence'][item.position - 1]:
                        if len(social_items[item.sku]['sequence']) > item.position:
                            item.quantity += 1
                            item.position += 1

                else:
                    print('Got a nextStep with an out of bound sequence index !')

            else:
                print('Got a nextStep on a social item that has no listSequence !')

        elif action == 'buyItem':
            item = self.user.profile.social_items.filter_by(sku=self.command_data['sku']).first()

            # Ubisoft devs are again clowning me, sometimes socialItems field is in the transaction object
            # Which should always happen so handle_transaction() can increment the given social item quantity
            # But no idea why this field is missing when you buy stuff in battle

            use_transaction = self.command_data['transaction'].get('socialItems') is not None

            if item is None:  # Means the user bought an item he doesn't have yet
                item = SocialItem(
                    sku=self.command_data['sku'],
                    quantity=int(not use_transaction)
                )

                self.user.profile.social_items.append(item)

            else:
                if not use_transaction:
                    item.quantity += 1

        elif action == 'applyCrafting':
            if self.command_data['sku'] in crafting_rewards:
                reward_item_sku = crafting_rewards[self.command_data['sku']]

                item = self.user.profile.social_items.filter_by(sku=reward_item_sku).first()

                if item is not None:
                    item.quantity += 1

                else:
                    self.user.profile.social_items.append(SocialItem(
                        sku=reward_item_sku,
                        quantity=1
                    ))

            else:
                print('Got an unknow item crafted: {}'.format(self.command_data['sku']))

        elif action == 'useItem':
            item_sku = self.command_data['sku']

            item = self.user.profile.social_items.filter_by(sku=item_sku).first()

            if item is not None:
                if item.quantity > 0:
                    item.quantity -= 1

                if item_sku in use_action_reward:
                    item_reward_info = use_action_reward[item_sku]
                    reward_type = item_reward_info['type']

                    if reward_type == 'ressources':
                        ressource_type = item_reward_info['ressourceType']

                        if item_reward_info['percent']:
                            if ressource_type == 'coins':
                                amount = (self.user.profile.max_coins) / 100 * item_reward_info['amount']

                            elif ressource_type == 'minerals':
                                amount = (self.user.profile.max_minerals) / 100 * item_reward_info['amount']

                            else:
                                print('Usage of percent on something else than coins or minerals: {}'.format(ressource_type))
                                return False

                        else:
                            amount = item_reward_info['amount']

                        setattr(self.user.profile, ressource_type, getattr(self.user.profile, ressource_type) + amount)

                    elif reward_type == 'item':
                        reward_item = self.user.profile.social_items.filter_by(sku=item_reward_info['rewardSku']).first()

                        if reward_item is not None:
                            reward_item.quantity += item_reward_info['amount']

                        else:
                            self.user.profile.social_items.append(SocialItem(
                                sku=item_reward_info['rewardSku'],
                                quantity=item_reward_info['amount']
                            ))

                    elif reward_type == 'powerUp':
                        power_up = self.user.profile.power_ups.filter_by(sku=item_reward_info['sku']).first()

                        if power_up is not None:
                            power_up.end_time = datetime.utcnow() + timedelta(hours=item_reward_info['duration'])

                        else:
                            self.user.profile.power_ups.append(PowerUp(
                                sku=item_reward_info['sku'],
                                end_time=datetime.utcnow() + timedelta(hours=item_reward_info['duration'])
                            ))

                    elif reward_type == 'sequence':
                        if len(item_reward_info['sequence']) > item.position:
                            item_sequence_reward = item_reward_info['sequence'][item.position]
                            item_sequence_reward_type = item_sequence_reward['type']

                            if item_sequence_reward_type == 'ressources':
                                ressource_type = item_sequence_reward['ressourceType']

                                if item_sequence_reward['percent']:
                                    if ressource_type == 'coins':
                                        amount = (self.user.profile.total_coins_storage + 9000) / 100 * item_sequence_reward['amount']

                                    elif ressource_type == 'minerals':
                                        amount = (self.user.profile.total_minerals_storage + 9000) / 100 * item_sequence_reward['amount']

                                    else:
                                        print('Usage of percent on something else than coins or minerals: {}'.format(ressource_type))
                                        return False

                                else:
                                    amount = item_sequence_reward['amount']

                                setattr(self.user.profile, ressource_type, getattr(self.user.profile, ressource_type) + amount)

                            elif item_sequence_reward_type == 'item':
                                reward_item = self.user.profile.social_items.filter_by(sku=item_sequence_reward['rewardSku']).first()

                                if reward_item is not None:
                                    reward_item.quantity += item_sequence_reward['amount']

                                else:
                                    self.user.profile.social_items.append(SocialItem(
                                        sku=item_sequence_reward['rewardSku'],
                                        quantity=item_sequence_reward['amount']
                                    ))

                            if item.position == len(item_reward_info['sequence']) - 1:
                                item.position = 0

                            else:
                                item.position += 1

            else:
                print('An user tried to use an item he doesn\'t own: {}'.format(item_sku))

        elif action == 'removeItem':
            item = self.user.profile.social_items.filter_by(sku=self.command_data['sku']).first()

            if item is not None:
                item.quantity -= self.command_data['amount']

            else:
                print('An user tried to remove an item he doesn\'t own: {}'.format(self.command_data['sku']))

        self.handle_transaction()
        self.user.profile.save()
