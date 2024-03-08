from command.base_command import BaseCommand

from database.models.user.profile import UserProfile


class GetNeighboursHandler(BaseCommand):

    def answer(self):
        self.answer_command_data[self.command_data['type']] = []

        if self.command_data['type'] == 'pending':
            for pending_request in self.user.profile.outgoing_neighbour_requests:
                neighbour_info = {}

                neighbour_info['userId'] = pending_request.ReceiverProfile.id
                neighbour_info['requestId'] = pending_request.id
                neighbour_info['name'] = pending_request.ReceiverProfile.username
                neighbour_info['platform'] = ''
                neighbour_info['platformId'] = ''

                self.answer_command_data['pending'].append(neighbour_info)

        elif self.command_data['type'] == 'incoming':
            for incoming_request in self.user.profile.incoming_neighbour_requests:
                neighbour_info = {}

                neighbour_info['userId'] = incoming_request.SenderProfile.id
                neighbour_info['requestId'] = incoming_request.id
                neighbour_info['name'] = incoming_request.SenderProfile.username
                neighbour_info['platform'] = ''

                self.answer_command_data['incoming'].append(neighbour_info)

        else:
            for neighbour in self.user.profile.neighbours:
                neighbour_profile = UserProfile.query.get(neighbour.friend_id)

                if neighbour_profile is not None:
                    neighbour_info = {}
                    neighbour_info['userId'] = neighbour_profile.id
                    neighbour_info['name'] = neighbour_profile.username
                    neighbour_info['platform'] = ''
                    neighbour_info['avatar'] = neighbour_profile.avatar
                    neighbour_info['isMuted'] = False

                    if neighbour_profile.has_alliance:
                        neighbour_info['allianceName'] = neighbour_profile.Alliance.name
                        neighbour_info['allianceLogo'] = neighbour_profile.Alliance.logo

                    self.answer_command_data['confirmed'].append(neighbour_info)
