from command.base_command import BaseCommand

from database.models.user.social.neighbour import Neighbour


class AcceptNeighbourHandler(BaseCommand):

    def answer(self):
        request = self.user.profile.incoming_neighbour_requests.filter_by(id=self.command_data['requestId']).first()

        if request is not None:
            self.user.profile.neighbours.append(Neighbour(friend_id=request.sender_profile_id))
            request.SenderProfile.neighbours.append(Neighbour(friend_id=request.receiver_profile_id))

            request.delete()

        else:
            self.answer_command_data['status'] = 'ERROR'
