from command.base_command import BaseCommand
# from database.models.user.user import User
from database.models.user.social.message import Message


class ReadMessageHandler(BaseCommand):

    def process(self):
        message = Message.query.get(self.command_data['id'])

        if message is not None:
            message.delete()

        else:
            print('An user tried to delete an unknown message: {}'.format(self.command_data['id']))
