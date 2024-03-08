from command.base_command import BaseCommand


class UpdateAvatarHandler(BaseCommand):

    def process(self):
        self.user.profile.avatar = self.command_data['avatar']

        self.handle_transaction()
        self.user.profile.save()
