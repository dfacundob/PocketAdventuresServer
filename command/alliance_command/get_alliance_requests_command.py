from datetime import datetime, timedelta

from command.base_command import BaseCommand
from database.models.user.profile import UserProfile
from database.models.alliances.alliance_invite import AllianceInvite
from database.models.alliances.alliance_request import AllianceRequest
from utils.enums import ALLIANCE_INVITE


class GetAllianceRequestHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['result'] = {}
        self.answer_command_data['result']['requests'] = []

        if self.user.profile.has_alliance:
            for request in self.user.profile.Alliance.requests.filter(AllianceRequest.sent_date >= datetime.utcnow() - timedelta(days=3)):
                sender_profile = UserProfile.query.get(request.user_id)

                request_info = {}
                request_info['allianceId'] = request.Alliance.id
                request_info['allianceName'] = request.Alliance.name
                request_info['expiryTime'] = request.expiry_time
                request_info['time'] = int(datetime.utcnow().timestamp() * 1000)
                request_info['time'] = request.sent_at
                request_info['message'] = ''
                request_info['senderAvatar'] = sender_profile.avatar
                request_info['senderId'] = sender_profile.id
                request_info['senderName'] = sender_profile.username
                request_info['type'] = ALLIANCE_INVITE.JOIN
                request_info['senderLevel'] = sender_profile.level_based_on_score
                request_info['senderPlanets'] = sender_profile.planets.count()

                self.answer_command_data['result']['requests'].append(request_info)

        for request in self.user.profile.incoming_alliance_invites.filter(AllianceInvite.sent_date >= datetime.utcnow() - timedelta(days=3)):
            request_info = {}

            request_info['allianceId'] = request.alliance_id
            request_info['allianceName'] = request.alliance_name
            request_info['expiryTime'] = request.expiry_time
            request_info['time'] = int(datetime.utcnow().timestamp() * 1000)
            request_info['message'] = ''  # not used
            request_info['senderAvatar'] = request.SenderProfile.avatar
            request_info['senderId'] = request.SenderProfile.id
            request_info['senderName'] = request.SenderProfile.username
            request_info['type'] = request.type
            request_info['senderLevel'] = request.SenderProfile.level_based_on_score
            request_info['senderPlanets'] = request.SenderProfile.planets.count()

            self.answer_command_data['result']['requests'].append(request_info)
