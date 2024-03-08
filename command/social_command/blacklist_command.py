from command.base_command import BaseCommand

from database.models.user.profile import UserProfile
from database.models.user.social.muted_user import MutedUser


class BlacklistHandler(BaseCommand):

    def answer(self):
        action = self.command_data['action']

        if action == 'list':
            self.answer_command_data['muted'] = []

            for muted_user in self.user.profile.muted_users:
                muted_user_profile = UserProfile.query.get(muted_user.user_id)

                if muted_user_profile is not None:
                    muted_user_info = {}

                    muted_user_info['userId'] = muted_user.user_id
                    muted_user_info['name'] = muted_user_profile.username
                    muted_user_info['platform'] = ''
                    muted_user_info['avatar'] = muted_user_profile.avatar

                    self.answer_command_data['muted'].append(muted_user_info)

        elif action == 'mute':
            self.user.profile.muted_users.append(MutedUser(
                user_id=self.command_data['userId']
            ))

            self.user.profile.save()

        elif action == 'unmute':
            muted_user = self.user.profile.muted_users.filter_by(
                user_id=self.command_data['userId']
            ).first()

            if muted_user is not None:
                muted_user.delete()
