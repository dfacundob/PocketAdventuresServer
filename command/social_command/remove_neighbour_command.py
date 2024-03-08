from command.base_command import BaseCommand

from database.models.user.social.neighbour import Neighbour


class RemoveNeighbourHandler(BaseCommand):

    def answer(self):
        neighbour = self.user.profile.neighbours.filter_by(friend_id=self.command_data['targetId']).first()

        neighbour_request = Neighbour.query.filter_by(user_profile_id=self.command_data['targetId'],
                                                      friend_id=self.user.profile.id).first()

        if neighbour and neighbour_request:
            neighbour.delete()
            neighbour_request.delete()

        else:
            self.answer_command_data['status'] = 'ERROR'
