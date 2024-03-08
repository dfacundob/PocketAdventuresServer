from command.base_command import BaseCommand


class IgnoreNeighbourHandler(BaseCommand):

    def answer(self):
        request = self.user.profile.incoming_neighbour_requests.filter_by(id=self.command_data['requestId']).first()

        if request is not None:
            request.delete()

        else:
            self.answer_command_data['status'] = 'ERROR'
