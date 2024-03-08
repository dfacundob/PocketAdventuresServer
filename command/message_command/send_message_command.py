from command.base_command import BaseCommand
from database.models.user.user import UserProfile
from database.models.user.social.message import Message


class SendMessageHandler(BaseCommand):

    def process(self):
        receiver = UserProfile.query.get(self.command_data['sentTo'])
        is_blacklisted = receiver.muted_users.filter_by(user_id=self.user.profile.id).first() is not None

        if receiver is not None:
            if not is_blacklisted:
                receiver.messages.append(Message(
                    sender_id=self.user.id,
                    sender_name=self.user.profile.username,
                    message=self.command_data['message'])
                )

                receiver.save()

        else:
            print('An user tried to send a message to an unknown user: {}'.format(self.command_data['sentTo']))
