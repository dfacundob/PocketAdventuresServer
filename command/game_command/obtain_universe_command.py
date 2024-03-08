import copy

from datetime import datetime
from utils.enums import PLAY_MODE
from database.models.user.user import User
from database.models.battle.battle import Battle
from database.models.galaxy.planet.planet import Planet

from command.base_command import BaseCommand


class ObtainUniverseHandler(BaseCommand):

    def process(self):
        self.is_base_owner = False
        self.is_attacking = False
        self.is_requesting_npc = False

        if self.command_data.get('targetAdvisorSku') is not None:
            # mean we ask for a NPC base
            self.is_requesting_npc = True

            if self.command_data['attack']:
                self.user.profile.total_attacks_done += 1
                self.user.profile.play_mode = PLAY_MODE.ATTACKING_NPC
                self.user.profile.npcs.last_attacked = self.command_data['targetAdvisorSku']
                self.user.profile.npcs.update_last_attack_date(self.command_data['targetAdvisorSku'])

            else:
                self.user.profile.play_mode = PLAY_MODE.VISITING

        else:
            target_user_id = self.command_data['targetAccountId']

            target_user = User.query.get(target_user_id)

            if target_user == self.user:
                self.is_base_owner = True
                self.user.profile.play_mode = PLAY_MODE.PLAYING
                self.user.profile.actual_planet_index = self.command_data['planetId'] - 1

            else:
                if self.command_data['attack']:
                    self.user.profile.play_mode = PLAY_MODE.ATTACKING
                    self.user.profile.total_attacks_done += 1
                    self.user.profile.protection_end_time = datetime.utcnow()  # Remove the attacker shield

                    target_user.profile.total_attacks_received += 1

                else:
                    self.user.profile.play_mode = PLAY_MODE.VISITING

            if target_user is not None:
                self.target_user = target_user.profile
                self.target_planet = self.target_user.planets.filter_by(planet_id=self.command_data['planetId']).first()

                if self.target_planet is not None:
                    if self.user.profile.is_war_opponent(target_user.profile) and self.target_planet.damage_percent >= 75:
                        self.target_planet.repair()

                    if self.command_data['attack']:
                        self.user.profile.last_attack_planet_id = self.target_planet.id

                else:
                    print('An user tried to obtain a unknown planet (id: {}) of the user {}'.format(self.command_data['planetId'], target_user.profile))
                    return False

            else:
                print('An user tried to obtain universe of an unknown user {}'.format(self.command_data['targetAccountId']))
                return False

        self.handle_transaction()
        self.user.profile.save()

    def answer(self):
        self.answer_command_data['events'] = []
        self.answer_command_data['promo'] = None

        self.answer_command_data['Universe'] = []

        if self.is_requesting_npc:
            npc_universe = self.user.profile.npcs.get_npc_base(self.command_data['targetAdvisorSku'])

            if npc_universe is not None:
                self.answer_command_data['Universe'] = npc_universe

            else:
                print('An unknown npc got requested: {}'.format(self.command_data['targetAdvisorSku']))
                return False

        else:
            self.answer_command_data['friendCode'] = self.target_user.friend_code
            ############ Profile part ############

            user_profile_data = {}
            user_profile_data['Profile'] = []

            # user_profile_data['lastCashBoughtDate'] = int(datetime.utcnow().timestamp() * 1000) - 12000000
            # user_profile_data['LastFreeChipShownTime'] = int(datetime.utcnow().timestamp() * 1000) - 12000000
            # user_profile_data['startedDate'] = int(datetime.utcnow().timestamp() * 1000) - 24000000

            user_profile_data['exp'] = self.target_user.xp
            user_profile_data['DCCoins'] = self.target_user.coins  # Player Coins
            user_profile_data['DCMinerals'] = self.target_user.minerals  # Player Minerals
            user_profile_data['DCCash'] = self.target_user.chips  # Player Chips
            user_profile_data['playerName'] = self.target_user.username  # Player Name
            user_profile_data['DCWorldName'] = self.target_user.world_name  # Player World Name

            user_profile_data['flags'] = ','.join(['{}:{}'.format(flag.key, flag.value) for flag in self.target_user.flags])

            user_profile_data['DCPlayerRank'] = 1
            user_profile_data['DCDroids'] = self.target_planet.droids  # Player worker count
            user_profile_data['tutorialCompleted'] = self.target_user.is_tutorial_completed
            user_profile_data['damageProtectionTimeLeft'] = self.target_user.protection_time_left  # Time as milliseconds
            user_profile_data['damageProtectionTimeTotal'] = 0

            user_profile_data['totalCoinsLooted'] = self.target_user.total_coins_looted
            user_profile_data['totalMineralsLooted'] = self.target_user.total_minerals_looted
            user_profile_data['totalBasesDestroyed'] = self.target_user.total_bases_destroyed
            user_profile_data['totalAttacksDone'] = self.target_user.total_attacks_done
            user_profile_data['totalBasesLost'] = self.target_user.total_bases_lost
            user_profile_data['totalAttacksReceived'] = self.target_user.total_attacks_received

            if self.is_base_owner:
                user_profile_data['lastVisitTime'] = self.target_planet.last_visit_time  # Time in milliseconds since latest visit
                self.target_planet.last_visit_time = datetime.utcnow()
                self.user.profile.save()

            user_profile_data['lastLevelNotified'] = self.target_user.last_level_notified
            user_profile_data['score'] = self.target_user.score  # Player XP

            user_profile_data['avatar'] = self.target_user.avatar

            user_profile_data['powerUps'] = {}

            for power_up in self.target_user.power_ups:
                user_profile_data['powerUps'][power_up.sku] = power_up.time_left

            profile_data = {}

            profile_data['Missions'] = []

            missions_types = ['ReadyToStart', 'Available', 'Unlocked', 'Rewarded', 'Completed', 'Params']

            missions_types_state = {
                'ReadyToStart': 1,
                'Available': 2,
                'Rewarded': 3,
                'Completed': 4
            }

            for mission_type in missions_types:
                missions = {}
                missions[mission_type] = ''

                if mission_type in missions_types_state:
                    user_missions = self.target_user.missions.filter_by(state=missions_types_state[mission_type]).all()

                    missions['chunk'] = ','.join([mission.sku for mission in user_missions])

                else:
                    missions['chunk'] = ''

                profile_data['Missions'].append(missions)

            profile_data['Targets'] = []

            for mission in self.target_user.missions:
                profile_data['Targets'].append({'progress': ':'.join([mission.sku, mission.progress])})

            profile_data['baseCoinsAndMineralsCapacity'] = self.target_user.starbase_capacity  # Coins & Minerals the starbase can contains

            profile_data['Planets'] = []

            for planet in self.target_user.planets.order_by(Planet.planet_id.asc()):  # Gotta order it else the game is fucked up
                profile_data['Planets'].append(planet.encode())

            user_profile_data['Profile'].append(profile_data)

            user_profile_data['expendables'] = None

            self.answer_command_data['Universe'].append(user_profile_data)

            world_data = {}
            world_data['World'] = []

            items_data = {}
            items_data['Items'] = []

            for item in self.target_planet.items:
                item_data = {}

                item_data['sku'] = item.sku
                item_data['sid'] = item.sid
                item_data['upgradeId'] = item.upgrade_id
                item_data['time'] = item.time
                item_data['state'] = item.state
                item_data['x'] = item.x
                item_data['y'] = item.y
                item_data['type'] = item.type
                item_data['isFlipped'] = item.is_flipped
                item_data['repairing'] = item.repairing
                item_data['incomeToRestore'] = item.income_to_restore
                item_data['energy'] = item.energy

                items_data['Items'].append(item_data)

            world_data['World'].append(items_data)

            game_units_data = {}
            game_units_data['GameUnits'] = []

            for game_unit in self.target_planet.game_units:
                game_units_data['GameUnits'].append(game_unit.encode())

            world_data['World'].append(game_units_data)

            shipyards_data = {}
            shipyards_data['Shipyards'] = []

            for shipyard in self.target_planet.shipyards:
                shipyard_data = {}
                shipyard_data['sid'] = shipyard.sid
                shipyard_data['unlockedSlots'] = shipyard.unlocked_slots

                shipyard_data['Shipyard'] = []

                slots_data = {}
                slots_data['Slots'] = []

                for slot in shipyard.slots:
                    if slot.ships_sku is not None:
                        slot_data = {}
                        slot_data['sku'] = slot.ships_sku
                        slot_data['Slot'] = []

                        for ship in slot.ships:
                            ship_data = {}
                            ship_data['Ship'] = ''
                            ship_data['timeLeft'] = ship.time_left

                            slot_data['Slot'].append(ship_data)

                        slots_data['Slots'].append(slot_data)

                shipyard_data['Shipyard'].append(slots_data)

                shipyards_data['Shipyards'].append(shipyard_data)

            world_data['World'].append(shipyards_data)

            hangars_data = {}
            hangars_data['Hangars'] = []

            for hangar in self.target_planet.hangars:
                hangar_data = {}
                hangar_data['sid'] = hangar.sid

                hangar_data['Hangar'] = []

                for ship in hangar.hangar_ships:
                    ship_data = {}
                    ship_data['sku'] = ship.sku

                    hangar_data['Hangar'].append(ship_data)

                hangars_data['Hangars'].append(hangar_data)

            world_data['World'].append(hangars_data)

            bunkers_data = {}
            bunkers_data['Bunkers'] = []

            for bunker in self.target_planet.bunkers:
                bunker_data = {}
                bunker_data['sid'] = bunker.sid

                bunker_data['Bunker'] = []

                for ship in bunker.bunker_ships:
                    ship_data = {}
                    ship_data['sku'] = ship.sku

                    bunker_data['Bunker'].append(ship_data)

                bunkers_data['Bunkers'].append(bunker_data)

            world_data['World'].append(bunkers_data)

            self.answer_command_data['Universe'].append(world_data)

            if self.command_data['attack']:
                Battle(
                    attacker=self.user.profile,
                    receiver=self.target_user,
                    target_planet=self.target_planet,
                    attacker_planet=self.user.profile.current_planet,
                    universe=copy.deepcopy(self.answer_command_data)
                ).save()
