from command.base_command import BaseCommand

from database.models.user.profile import UserProfile
from database.models.user.social.neighbour_request import NeighbourRequest


class AddNeighbourHandler(BaseCommand):

    def process(self):
        receiver = UserProfile.query.filter_by(friend_code=self.command_data['code']).first()

        if receiver is not None:
            if receiver.id != self.user.profile.id:
                already_sent = self.user.profile.outgoing_neighbour_requests.filter_by(receiver_profile_id=receiver.id).first() is not None

                if not already_sent:
                    NeighbourRequest(
                        sender_profile_id=self.user.profile.id,
                        receiver_profile_id=receiver.id
                    ).save()

                else:
                    self.answer_command_data['status'] = 'ERROR'

            else:
                self.answer_command_data['status'] = 'ERROR'

        else:
            self.answer_command_data['status'] = 'ERROR'
