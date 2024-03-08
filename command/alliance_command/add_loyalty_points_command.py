from command.base_command import BaseCommand
from utils.enums import PLAY_MODE


class AddLoyaltyPointsHandler(BaseCommand):

    def process(self):
        if self.user.profile.has_alliance:
            # Loyalty points also get given when enabling an alliance powerup so we gotta make sure they are given during a war attack
            if self.user.profile.play_mode == PLAY_MODE.ATTACKING:
                if self.user.profile.Alliance.is_at_war:
                    self.user.profile.Alliance.current_war_damage += self.command_data['amount']
                    self.user.profile.Alliance.save()

                else:
                    print('An user got gifted loyalty points for a war attack but his alliance isn\'t at war: {}'.format(self.user.profile.id))

        else:
            print('An user got gifted loyalty points but doesn\'t belong to any alliance: {}'.format(self.user.profile.id))
