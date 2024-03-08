from datetime import datetime, timedelta
from command.base_command import BaseCommand
from database.models.galaxy.planet.bunkers.bunker_ship import BunkerShip
from database.models.galaxy.planet.hangars.hangar_ship import HangarShip
from database.models.galaxy.planet.shipyards.shipyard_ship import ShipyardShip
from database.models.galaxy.planet.shipyards.shipyard_slot import ShipyardSlot


class UpdateShipsHandler(BaseCommand):

    def process(self):
        action = self.command_data['action']
        planet = self.user.profile.current_planet

        if action == 'shipAdded':
            shipyard = planet.shipyards.filter_by(sid=self.command_data['sid']).first()

            if shipyard is not None:
                slot_index = self.command_data['slot']

                if len(shipyard.slots.all()) >= slot_index + 1:
                    slot = shipyard.slots[slot_index]

                    slot.ships_sku = self.command_data['sku']

                    if not slot.ships.all():
                        end_time = datetime.utcnow() + timedelta(milliseconds=self.command_data['timeLeft'])

                    else:
                        end_time = slot.ships.order_by(ShipyardShip.id.desc()).first().end_time + timedelta(milliseconds=self.command_data['timeLeft'])

                    slot.ships.append(ShipyardShip(
                        end_time=end_time
                    ))

                else:
                    print('An user tried to train units in a slot he doesn\'t have access to: {}'.format(slot_index))

            else:
                print('An user tried to train unit in an unknown shipyard: {}'.format(self.command_data['sid']))

        elif action == 'shipRemoved':
            shipyard = planet.shipyards.filter_by(sid=self.command_data['sid']).first()

            if shipyard is not None:
                slot_index = self.command_data['slot']

                if len(shipyard.slots.all()) >= slot_index + 1:
                    slot = shipyard.slots.filter_by(ships_sku=self.command_data['sku']).first()

                    if slot is not None:
                        slot.ships.order_by(ShipyardShip.id.desc()).first().delete()

                        if not slot.ships.all():
                            slot.ships_sku = None

                    else:
                        print('An user tried to remove an unit he didn\'t trained: {}'.format(self.user.profile.id))

                else:
                    print('An user tried to delete units in a slot he doesn\'t have access to: {}'.format(slot_index))

            else:
                print('An user tried to delete an unit from an unknown shipyard: {}'.format(self.command_data['sid']))

        elif action == 'shipCompleted':
            shipyard = planet.shipyards.filter_by(sid=self.command_data['sid']).first()

            slot = shipyard.slots.filter_by(ships_sku=self.command_data['sku']).first()

            if slot is not None:
                slot.ships.first().delete()

                if not slot.ships.all():
                    slot.ships_sku = None

                hangar = planet.hangars.filter_by(sid=self.command_data['hangarSid']).first()

                if hangar is not None:
                    hangar.hangar_ships.append(HangarShip(
                        sku=self.command_data['sku']
                    ))

                else:
                    print('Unit sent to an unknow hangar: {}'.format(self.command_data['hangarSid']))

            else:
                print('An unit finished to be trained from an unknown slot: {}'.format(self.command_data))

        elif action == 'killUnitFromHangar':
            hangar = planet.hangars.filter_by(sid=self.command_data['hangarSid']).first()

            if hangar is not None:
                unit = hangar.hangar_ships.filter_by(sku=self.command_data['unitSku']).first()

                if unit is not None:
                    unit.delete()

                else:
                    print('An unknown unit got killed from hangar: {}'.format(self.command_data['unitSku']))

            else:
                print('An unit got killed from an unknown hangar: {}'.format(self.command_data['hangarSid']))

        elif action == 'moveFromHangarToBunker':
            hangar = planet.hangars.filter_by(sid=self.command_data['hangarSid']).first()
            bunker = planet.bunkers.filter_by(sid=self.command_data['bunkerSid']).first()

            if hangar and bunker:
                unit = hangar.hangar_ships.filter_by(sku=self.command_data['unitSku']).first()

                if unit is not None:
                    bunker.bunker_ships.append(BunkerShip(
                        sku=unit.sku
                    ))

                    unit.delete()

                else:
                    print('An unknow unit got sent from hangar to bunker: {}'.format(self.command_data['unitSku']))

            else:
                print('An unit got sent from an hangar ({}) to a bunker ({}) but one of thoses don\'t exists'.format(
                    self.command_data['hangarSid'],
                    self.command_data['bunkerSid']
                ))

        elif action == 'killUnitFromBunker':
            bunker = planet.bunkers.filter_by(sid=self.command_data['bunkerSid']).first()

            if bunker is not None:
                unit = bunker.bunker_ships.filter_by(sku=self.command_data['unitSku']).first()

                if unit is not None:
                    unit.delete()

                else:
                    print('An unknown unit got killed from bunker: {}'.format(self.command_data['unitSku']))

            else:
                print('An unit got killed from an unknown bunker: {}'.format(self.command_data['bunkerSid']))

        elif action == 'addSlot':
            shipyard = planet.shipyards.filter_by(sid=self.command_data['sid']).first()

            if shipyard is not None:
                shipyard.unlocked_slots += 1
                shipyard.slots.append(ShipyardSlot())

            else:
                print('An user tried to unlock a slot on an unknown shipyard: {}'.format(self.command_data['sid']))

        elif action == 'speedUp':
            shipyard = planet.shipyards.filter_by(sid=self.command_data['sid']).first()

            if shipyard is not None:
                for unit in self.command_data['slotsContentsAccelerated']:
                    slot_index = unit['slot']

                    if len(shipyard.slots.all()) >= slot_index + 1:
                        slot = shipyard.slots.filter_by(ships_sku=unit['sku']).first()

                        slot.ships.order_by(ShipyardShip.id.desc()).first().delete()

                        if not slot.ships.all():
                            slot.ships_sku = None

                        hangar = planet.hangars.filter_by(sid=unit['hangarSid']).first()

                        if hangar is not None:
                            hangar.hangar_ships.append(HangarShip(
                                sku=unit['sku']
                            ))

                        else:
                            print('Unit sent to an unknow hangar: {}'.format(unit['hangarSid']))

                    else:
                        print('An user tried to delete units in a slot he doesn\'t have access to: {}'.format(slot_index))

            else:
                print('An user tried to speedUp unit from an unknown shipyard: {}'.format(self.command_data['sid']))

        elif action == 'giftUnitToHangar':
            hangar = planet.hangars.filter_by(sid=self.command_data['hangarSid']).first()

            if hangar is not None:
                for _ in range(self.command_data['amount']):
                    hangar.hangar_ships.append(HangarShip(
                        sku=self.command_data['unitSku']
                    ))

            else:
                print('An user have been gifted an unit to an unknown hangar: {}'.format(self.command_data['hangarSid']))

        self.handle_transaction()
        self.user.profile.save()
