import json

from command.base_command import BaseCommand

from database.models.user.profile import UserProfile
from database.models.galaxy.planet.planet import Planet


class ManageAllianceMembersHandler(BaseCommand):

    def answer(self):
        action = self.command_data['action']

        self.answer_command_data['requestParams'] = {}
        self.answer_command_data['requestParams']['action'] = action

        self.answer_command_data['responseJSON'] = {}

        # We are not handling getCandidate since it break the game :/
        if action == 'getMember':
            user_id = int(self.command_data['memberId'])

            self.answer_command_data['responseJSON']['id'] = user_id

            if user_id == self.user.profile.id:
                # Usefull to know who you sent invite & requests to (probably used to avoid sending requests twice or more)
                invites_info = {}

                for request in self.user.profile.outgoing_alliance_invites:
                    invites_info[request.receiver_profile_id] = request.sent_at

                self.answer_command_data['responseJSON']['invitesSent'] = json.dumps(invites_info)
                self.answer_command_data['responseJSON']['requestsSent'] = ''

            if not user_id == self.user.profile.id:
                user_profile = UserProfile.query.get(user_id)

                self.answer_command_data['responseJSON']['planets'] = []

                for planet in user_profile.planets.order_by(Planet.planet_id.asc()):
                    planet_info = {}

                    planet_info['HQLevel'] = planet.hq_level
                    planet_info['planetId'] = planet.planet_id
                    planet_info['starName'] = planet.Galaxy.name
                    planet_info['sku'] = planet.sku

                    # Gotta append twice cuz of ubisoft clowns
                    self.answer_command_data['responseJSON']['planets'].append(planet_info)
                    self.answer_command_data['responseJSON']['planets'].append(None)
