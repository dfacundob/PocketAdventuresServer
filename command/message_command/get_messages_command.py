# from base64 import b64encode
# from datetime import datetime

from command.base_command import BaseCommand


class GetMessagesHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['messages'] = []

        for message in self.user.profile.messages.all():
            message_data = {}

            message_data['id'] = message.id
            message_data['from'] = message.sender_name
            message_data['fromId'] = message.sender_id
            message_data['message'] = message.message
            message_data['time'] = str(message.time)

            self.answer_command_data['messages'].append(message_data)
