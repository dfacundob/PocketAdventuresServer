import json

from datetime import datetime, timedelta

from database.models.user.flag import Flag
from command.base_command import BaseCommand
from utils.utils import protection_times, npc_bases


class UpdateProfileHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']

        if action == 'tutorialCompleted':
            self.user.profile.is_tutorial_completed = True
            self.user.profile.npcs.firebit_progress = 2  # Seems like they don't send a battleDamagesPack after the first Firebit attack
            self.user.profile.npcs.firebit_base = json.dumps(npc_bases['npc_B'][2])

        elif action == 'setDeviceName':
            self.user.profile.username = self.command_data['name']

        elif action in ('setFlag', 'setDeviceFlag'):
            flag = self.user.profile.flags.filter_by(key=self.command_data['key']).first()

            if flag is not None:
                flag.value = str(self.command_data['value'])

            else:
                self.user.profile.flags.append(Flag(
                    key=self.command_data['key'],
                    value=str(self.command_data['value'])
                ))

        elif action == 'exchangeCashToMinerals':
            self.user.profile.chips -= self.command_data['cash']
            self.user.profile.minerals += self.command_data['minerals']

        elif action == 'exchangeCashToCoins':
            self.user.profile.chips -= self.command_data['cash']
            self.user.profile.coins += self.command_data['coins']

        elif action == 'levelUp':
            self.user.profile.level_based_on_score = self.command_data['level']
            self.user.profile.last_level_notified = self.command_data['level']

        elif action == 'buyDroid':
            self.user.profile.current_planet.droids += 1

        elif action == 'buyDamageProtectionTime':
            if self.user.profile.has_shield:
                self.user.profile.protection_end_time += timedelta(hours=protection_times[self.command_data['sku']])

            else:
                self.user.profile.protection_end_time = datetime.utcnow() + timedelta(hours=protection_times[self.command_data['sku']])

        self.handle_transaction()
        self.user.profile.save()
