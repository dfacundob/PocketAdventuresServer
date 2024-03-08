from datetime import datetime, timedelta

from sqlalchemy import and_
from utils.enums import PLAY_MODE
from command.base_command import BaseCommand
from database.models.battle.battle import Battle
from database.models.battle.battle_event import BattleEvent


class UpdateBattleHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']

        if action == 'npcAttackStart':
            self.user.profile.play_mode = PLAY_MODE.UNDER_NPC_ATTACK

        elif action == 'battleDamagesPack':
            if self.user.profile.play_mode == PLAY_MODE.ATTACKING_NPC:
                npc_base = self.user.profile.npcs.attacked_npc_base
                npc_items = npc_base[1]['World'][0]['Items']
                npc_profile = npc_base[0]

                total_coins_looted = 0
                total_minerals_looted = 0
                increment_progress = False

                for info in self.command_data['pack']:
                    if info['action'] == 'itemDamaged':
                        item = None
                        item_sid = info['itemSid']

                        for item_info in npc_items:
                            if item_info['sid'] == item_sid:
                                item = item_info
                                break

                        if item is not None:
                            if info['destroyed']:
                                if item['sku'] == 'wonders_headquarters':
                                    increment_progress = True

                            if info['damage'] > 0:
                                item['energy'] -= info['damage']

                            self.handle_transaction(transaction_object=info['transaction'])

                            total_coins_looted += info['transaction']['coins']
                            total_minerals_looted += info['transaction']['minerals']
                            npc_profile['DCCoins'] += info['transactionTarget']['coins']
                            npc_profile['DCMinerals'] += info['transactionTarget']['minerals']

                        else:
                            print('An unknown npc item got damaged: {}'.format(item_sid))

                self.user.profile.total_coins_looted += total_coins_looted
                self.user.profile.total_minerals_looted += total_minerals_looted

                if increment_progress:
                    self.user.profile.npcs.increment_npc_progress()

                else:
                    self.user.profile.npcs.set_npc_base(self.user.profile.npcs.last_attacked, npc_base)

            elif self.user.profile.play_mode == PLAY_MODE.UNDER_NPC_ATTACK:
                planet = self.user.profile.current_planet

                for info in self.command_data['pack']:
                    pack_action = info['action']

                    # don't handle damaged item & units under npc attack (handle lost ressources though)
                    if pack_action == 'itemDamaged':
                        item = planet.items.filter_by(sid=info['itemSid']).first()

                        if item is not None:
                            self.handle_transaction(transaction_object=info['transaction'])

                        else:
                            print('An unknown item got damaged by npc: {}'.format(info['itemSid']))

            else:
                enemy_planet = self.user.profile.attacked_planet

                total_coins_looted = 0
                total_minerals_looted = 0

                for info in self.command_data['pack']:
                    pack_action = info['action']

                    if pack_action == 'itemDamaged':
                        item = enemy_planet.items.filter_by(sid=info['itemSid']).first()

                        if item is not None:
                            if info['destroyed']:
                                if item.sku == 'wonders_headquarters':
                                    self.user.profile.total_bases_destroyed += 1
                                    enemy_planet.UserProfile.total_bases_lost += 1

                                elif item.sku == 'hangar_001_001':
                                    hangar = enemy_planet.hangars.filter_by(sid=item.sid).first()

                                    if hangar is not None:
                                        for unit in hangar.hangar_ships:
                                            unit.delete()

                            if info['damage'] > 0:
                                item.energy -= info['damage']

                                enemy_planet.current_energy -= info['damage']

                            total_coins_looted += info['transaction']['coins']
                            total_minerals_looted += info['transaction']['minerals']

                            self.handle_transaction(transaction_object=info['transaction'])
                            self.handle_transaction(transaction_object=info['transactionTarget'], target_user=enemy_planet.UserProfile)

                        else:
                            print('An unknown item got damaged: {}'.format(info['itemSid']))

                    elif pack_action == 'unitDamaged':
                        if info['destroyed']:
                            bunker = enemy_planet.bunkers.filter_by(sid=info['fromBunkerSid']).first()

                            if bunker is not None:
                                unit = bunker.bunker_ships.filter_by(sku=info['unitSku']).first()

                                if unit is not None:
                                    total_coins_looted += info['transaction']['coins']
                                    total_minerals_looted += info['transaction']['minerals']

                                    self.handle_transaction(transaction_object=info['transaction'])
                                    unit.delete()

                                else:
                                    print('An unknown unit got destroyed from an ennemy bunker: {}'.format(info['unitSku']))

                            else:
                                print('An user destroyed an ennemy bunker unit from an unknown bunker: {}'.format(info['fromBunkerSid']))

                self.user.profile.total_coins_looted += total_coins_looted
                self.user.profile.total_minerals_looted += total_minerals_looted

                self.user.profile.current_battle.coins_taken += total_coins_looted
                self.user.profile.current_battle.minerals_taken += total_minerals_looted

        elif action == 'deployUnits':
            if self.user.profile.is_tutorial_completed:
                hangar = self.user.profile.current_planet.hangars.filter_by(sid=self.command_data['hangarSid']).first()

                if hangar is not None:
                    for unit_sku in self.command_data['unitsSkus']:
                        unit = hangar.hangar_ships.filter_by(sku=unit_sku).first()

                        # skuE = unit energy, skuSD = unit damage
                        if unit is not None:
                            if self.user.profile.play_mode != PLAY_MODE.ATTACKING_NPC:
                                self.user.profile.current_battle.events.append(BattleEvent(
                                    sku=unit_sku,
                                    x=self.command_data['x'],
                                    y=self.command_data['y'],
                                    time=self.command_data['millis']
                                ))

                            unit.delete()

                        else:
                            print('An user tried to deploy an unit he doesn\'t have in his hangar: {}'.format(unit_sku))

                else:
                    print('An user tried to deploy an unit from an unknown hangar: {}'.format(self.command_data['hangarSid']))

        elif action == 'specialAttack':
            item = self.user.profile.social_items.filter_by(sku=self.command_data['socialItemSku']).first()

            if item is not None:
                item.quantity -= 1

                if self.user.profile.play_mode != PLAY_MODE.ATTACKING_NPC:
                    self.user.profile.current_battle.events.append(BattleEvent(
                        sku='specialAttack_{}'.format(self.command_data['sku']),
                        x=self.command_data['x'],
                        y=self.command_data['y'],
                        time=self.command_data['millis']
                    ))

                self.handle_transaction()

            else:
                print('An user tried to use a special attack item he doesn\'t own: {}'.format(self.command_data['socialItemSku']))

        elif action == 'itemMineExploded':
            # We gotta check the user is attacking, ubisoft devs are so dumb that this command
            # is also sent when looking at a battle replay
            if self.user.profile.play_mode == PLAY_MODE.ATTACKING:
                mine = self.user.profile.attacked_planet.items.filter_by(sid=self.command_data['itemSid']).first()

                if mine is not None:
                    mine.delete()

                else:
                    print('An user tried to destroy an unknown mine: {}'.format(self.command_data['itemSid']))

        elif action == 'finished':
            if self.user.profile.play_mode not in (PLAY_MODE.ATTACKING_NPC, PLAY_MODE.UNDER_NPC_ATTACK):
                enemy_planet = self.user.profile.attacked_planet

                enemy_planet.UserProfile.lock_end_time = datetime.utcnow()

                self.user.profile.current_battle.events.append(BattleEvent(
                    sku='finished',
                    time=self.command_data['millis']
                ))

                # Calculate needed shield
                protection_time = 0

                if enemy_planet.damage_percent >= 75:
                    protection_time = 6

                elif enemy_planet.damage_percent >= 50:
                    protection_time = 2

                else:
                    if Battle.query.filter(and_(
                            Battle.receiver_profile_id == enemy_planet.UserProfile.id,
                            Battle.attacker_profile_id == self.user.profile.id,
                            Battle.attack_date >= datetime.utcnow() - timedelta(hours=1))) \
                            .count() >= 4:

                        protection_time = 1

                    elif Battle.query.filter(and_(
                            Battle.receiver_profile_id == enemy_planet.UserProfile.id,
                            Battle.attack_date >= datetime.utcnow() - timedelta(hours=24))) \
                            .count() >= 10:

                        protection_time = 6

                if protection_time:
                    enemy_planet.UserProfile.protection_end_time = datetime.utcnow() + timedelta(hours=protection_time)

            elif self.user.profile.play_mode == PLAY_MODE.UNDER_NPC_ATTACK:
                self.user.profile.play_mode = PLAY_MODE.PLAYING

        self.user.profile.save()
