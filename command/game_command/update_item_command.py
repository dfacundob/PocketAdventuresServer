from datetime import datetime, timedelta
from command.base_command import BaseCommand
from database.models.galaxy.planet.item import Item
from database.models.galaxy.planet.bunkers.bunker import Bunker
from database.models.galaxy.planet.hangars.hangar import Hangar
from database.models.galaxy.planet.shipyards.shipyard import Shipyard

from utils.utils import items_energy, items_time, silos_ressources


class UpdateItemHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']
        planet = self.user.profile.current_planet

        if action == 'newItem':
            item_info = self.command_data['item']

            item = Item(
                sku=item_info['sku'],
                sid=item_info['sid'],
                upgrade_id=item_info['upgradeId'],
                end_time=datetime.utcnow() + timedelta(milliseconds=item_info['time']),
                state=item_info['state'],
                x=item_info['x'],
                y=item_info['y'],
                type=item_info['type'],
                is_flipped=item_info['isFlipped'],
                repairing=item_info['repairing'],
                income_to_restore=item_info['incomeToRestore'],
                energy=item_info['energy']
            )

            planet.items.append(item)

            if item.calculate_energy:
                planet.total_energy += item_info['energy']
                planet.current_energy += item_info['energy']

        elif action == 'instantRepairAll':
            for item_data in self.command_data['items']:
                item = planet.items.filter_by(sid=item_data['sid']).first()

                if item is not None:
                    item.repairing = 0

                    if item.sku in items_energy:
                        item_full_energy = items_energy[item.sku][str(item.upgrade_id)]
                        planet.current_energy += (item_full_energy - item.energy)
                        item.energy = item_full_energy

                    else:
                        print('Building {} instant repaired: cannot find corresping energy value'.format(item.sku))

                else:
                    print('instantRepairAll on unknown item: {}'.format(item_data['sid']))

        else:
            item = planet.items.filter_by(sid=self.command_data['sid']).first()

            if item is not None:
                if action == 'newState':
                    item.state = self.command_data['newState']
                    item.end_time = datetime.utcnow() + timedelta(milliseconds=self.command_data['time'])

                    if self.command_data['oldState'] == 0 and self.command_data['newState'] == 1:  # means the building finished being built
                        if item.sku in silos_ressources:
                            item_info = silos_ressources[item.sku]

                            additional_storage = item_info['amount'][str(item.upgrade_id)]

                            if item_info['ressourceType'] == 'coins':
                                planet.coins_limit += additional_storage
                                self.user.profile.total_coins_storage += additional_storage

                            elif item_info['ressourceType'] == 'minerals':
                                planet.minerals_limit += additional_storage
                                self.user.profile.total_minerals_storage += additional_storage

                        if item.type == 3:
                            # means a shipyard got constructed
                            planet.shipyards.append(Shipyard(
                                sid=item.sid
                            ))

                        elif item.type == 7:
                            # means an hangar got constructed
                            planet.hangars.append(Hangar(
                                sid=item.sid
                            ))

                        elif item.type == 8:
                            # means a bunker got constructed
                            planet.bunkers.append(Bunker(
                                sid=item.sid
                            ))

                    elif self.command_data['oldState'] == 2 and self.command_data['newState'] == 1:  # means the building finished being upgraded
                        item.upgrade_id += 1

                        if item.sku in items_energy:
                            item.energy = items_energy[item.sku][str(item.upgrade_id)]

                            planet.total_energy += (items_energy[item.sku][str(item.upgrade_id)] - items_energy[item.sku][str(item.upgrade_id - 1)])
                            planet.current_energy += (items_energy[item.sku][str(item.upgrade_id)] - items_energy[item.sku][str(item.upgrade_id - 1)])

                        else:
                            print('Building {} upgraded: cannot find corresping new energy value'.format(item.sku))

                        if item.sku in silos_ressources:
                            item_info = silos_ressources[item.sku]
                            additional_storage = item_info['amount'][str(item.upgrade_id)] - item_info['amount'][str(item.upgrade_id - 1)]

                            if item_info['ressourceType'] == 'coins':
                                planet.coins_limit += additional_storage
                                self.user.profile.total_coins_storage += additional_storage

                            elif item_info['ressourceType'] == 'minerals':
                                planet.minerals_limit += additional_storage
                                self.user.profile.total_minerals_storage += additional_storage

                        if item.sku == 'wonders_headquarters':
                            planet.hq_level += 1

                    elif self.command_data['oldState'] == 1 and self.command_data['newState'] == 2:  # means the building is being upgraded
                        income_to_restore = self.command_data.get('incomeToRestore')

                        # Check to avoid upgrading a building more than it is possible (and avoid game crash)
                        if item.sku in items_energy:
                            if not str(item.upgrade_id + 1) in items_energy[item.sku]:
                                self.logout_player()

                        if income_to_restore is not None:
                            item.income_to_restore = income_to_restore

                    elif self.command_data['oldState'] == 1 and self.command_data['newState'] == 1:
                        item.income_to_restore = 0

                elif action == 'move':
                    item.x = self.command_data['x']
                    item.y = self.command_data['y']

                elif action == 'rotate':
                    item.x = self.command_data['x']
                    item.y = self.command_data['y']
                    item.is_flipped = self.command_data['flip']

                elif action == 'destroy':
                    if item.calculate_energy:
                        if item.sku in items_energy:
                            planet.total_energy -= items_energy[item.sku][str(item.upgrade_id)]
                            planet.current_energy -= item.energy

                    if item.sku in silos_ressources:
                        item_info = silos_ressources[item.sku]
                        lost_storage = item_info['amount'][str(item.upgrade_id)]

                        if item_info['ressourceType'] == 'coins':
                            planet.coins_limit -= lost_storage
                            self.user.profile.total_coins_storage -= lost_storage

                        elif item_info['ressourceType'] == 'minerals':
                            planet.minerals_limit -= lost_storage
                            self.user.profile.total_minerals_storage -= lost_storage

                    if item.type == 3:
                        shipyard = planet.shipyards.filter_by(sid=item.sid).first()

                        if shipyard is not None:
                            shipyard.delete()

                        else:
                            print('An unknown shipyard got destroyed: {}'.format(item.sid))

                    elif item.type == 7:
                        hangar = planet.hangars.filter_by(sid=item.sid).first()

                        if hangar is not None:
                            hangar.delete()

                        else:
                            print('An unknown hangar got destroyed: {}'.format(item.sid))

                    elif item.type == 8:
                        bunker = planet.bunkers.filter_by(sid=item.sid).first()

                        if bunker is not None:
                            bunker.delete()

                        else:
                            print('An unknown bunker got destroyed: {}'.format(item.sid))

                    item.delete()

                elif action in ('cancelBuild', 'instantRecicle'):
                    if item.calculate_energy:
                        planet.total_energy -= items_energy[item.sku][str(item.upgrade_id)]
                        planet.current_energy -= item.energy

                    item.delete()

                elif action == 'upgradePremium':
                    item.upgrade_id += 1

                    if item.sku in items_energy:
                        item.energy = items_energy[item.sku][str(item.upgrade_id)]

                        planet.total_energy += (items_energy[item.sku][str(item.upgrade_id)] - items_energy[item.sku][str(item.upgrade_id - 1)])
                        planet.current_energy += (items_energy[item.sku][str(item.upgrade_id)] - items_energy[item.sku][str(item.upgrade_id - 1)])

                    else:
                        print('Building {} premium upgraded: cannot find corresping new energy value'.format(item.sku))

                    if item.sku in items_time:
                        item.end_time = datetime.utcnow() + timedelta(milliseconds=items_time[item.sku][str(item.upgrade_id)])

                    if item.sku in silos_ressources:
                        item_info = silos_ressources[item.sku]
                        additional_storage = item_info['amount'][str(item.upgrade_id)] - item_info['amount'][str(item.upgrade_id - 1)]

                        if item_info['ressourceType'] == 'coins':
                            planet.coins_limit += additional_storage
                            self.user.profile.total_coins_storage += additional_storage

                        elif item_info['ressourceType'] == 'minerals':
                            planet.minerals_limit += additional_storage
                            self.user.profile.total_minerals_storage += additional_storage

                    if item.sku == 'wonders_headquarters':
                        planet.hq_level += 1

                elif action == 'cancelUpgrade':
                    item.state = 1
                    item.end_time = datetime.utcnow() + timedelta(milliseconds=self.command_data['time'])

                elif action == 'repairingStart':
                    item.repairing = 1

                elif action == 'repairingCompleted':
                    item.repairing = 0

                    if item.calculate_energy:
                        planet.current_energy += int(float(self.command_data['energy'])) - item.energy

                    item.energy = int(float(self.command_data['energy']))

            else:
                print('{} on unknown item'.format(action))
                return False

        self.handle_transaction()
        self.user.profile.save()
