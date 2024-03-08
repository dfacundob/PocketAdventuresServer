from datetime import datetime, timedelta

from command.base_command import BaseCommand
from database.models.user.user import User
from utils.errors import LOCK_ERROR


class QueryCheckAndLockAccountIfPossibleHandler(BaseCommand):

    def process(self):
        target_user = User.query.get(self.command_data['targetAccountId'])

        if target_user is not None:
            if target_user.profile.has_shield and not self.user.profile.is_war_opponent(target_user.profile):
                self.answer_command_data['lockType'] = LOCK_ERROR.USER_HAS_SHIELD

            elif target_user.is_online:
                self.answer_command_data['lockType'] = LOCK_ERROR.USER_ONLINE

            elif target_user.profile.is_under_attack:
                self.answer_command_data['lockType'] = LOCK_ERROR.USER_UNDER_ATTACK

            elif not target_user.profile.is_tutorial_completed:
                self.answer_command_data['lockType'] = LOCK_ERROR.USER_TUTORIAL_NOT_COMPLETED

            else:
                if self.command_data['applyLock']:
                    # 6 minutes instead of 5 so we are sure the user can't login at the very end of the battle cuz of
                    # the little cooldown due to the time btw QueryCheckAndLockAccountIfPossibleHandler and obtainUniverse
                    target_user.profile.lock_end_time = datetime.utcnow() + timedelta(minutes=6)
                    target_user.save()

                self.answer_command_data['lockSuccess'] = 1

        else:
            print('An user tried to lock an unknown account: {}'.format(self.command_data['targetAccountId']))
