from datetime import datetime

from command.base_command import BaseCommand
from database.models.user.profile import UserProfile
from database.models.alliances.alliance import Alliance
from database.models.alliances.alliance_request import AllianceRequest
from utils.enums import ALLIANCE_ROLE, LOG_TYPE
from utils.errors import ALLIANCE_ERROR


class AcceptAllianceRequestHandler(BaseCommand):

    def process(self):
        alliance = Alliance.query.get(self.command_data['aid'])

        if alliance is not None:
            if not alliance.is_full:
                request_type = self.command_data['messageType']

                if request_type == 'join':
                    if self.user.profile.has_alliance:
                        sender_id = self.command_data['senderId']
                        request = alliance.requests.filter_by(user_id=sender_id).first()

                        if request is not None:
                            sender_profile = UserProfile.query.get(sender_id)

                            if sender_profile is not None:
                                if not sender_profile.has_alliance:
                                    self.answer_command_data['senderId'] = sender_id
                                    self.answer_command_data['messageType'] = request_type

                                    alliance.members.append(sender_profile)

                                    alliance.add_log(
                                        subtype=LOG_TYPE.USER_JOINED,
                                        name=sender_profile.username,
                                        user_avatar=sender_profile.user_avatar,
                                        user_level=sender_profile.level_based_on_score
                                    )

                                    if alliance.is_at_war:
                                        sender_profile.role = ALLIANCE_ROLE.RECRUIT

                                    else:
                                        sender_profile.role = ALLIANCE_ROLE.REGULAR

                                    sender_profile.joined_alliance_time = datetime.utcnow()

                                    sender_profile.save()
                                    request.delete()

                                else:
                                    request.delete()
                                    self.answer_command_data['error'] = ALLIANCE_ERROR.DEFAULT_ERROR
                                    # Handle error code here TID_ALLIANCES_ALLIES_POPUP_CONFIRMLATE_BODY, seems like it's unused in the lib ffs

                            else:
                                print('An unknown user request got accepted: {}'.format(sender_id))

                        else:
                            # May happen if two admins accept the request at the same moment since alliance requests are badly refreshed
                            print('An user accepted an unknown alliance request from: {}'.format(sender_id))

                    else:
                        print('An user tried to accept an alliance request from an alliance he doesn\'t belong to: {}'.format(self.user.profile.id))

                else:
                    if not self.user.profile.has_alliance:
                        sender_id = self.command_data['senderId']

                        alliance_invite = self.user.profile.incoming_alliance_invites.filter_by(sender_profile_id=sender_id).first()

                        if alliance_invite is not None:
                            self.answer_command_data['senderId'] = sender_id
                            self.answer_command_data['messageType'] = request_type

                            if request_type == 'invite':
                                if not alliance.is_at_war:
                                    alliance.members.append(self.user.profile)

                                    alliance.add_log(
                                        subtype=LOG_TYPE.USER_JOINED,
                                        name=self.user.profile.username,
                                        user_avatar=self.user.profile.user_avatar,
                                        user_level=self.user.profile.level_based_on_score
                                    )

                                    self.user.profile.joined_alliance_time = datetime.utcnow()

                                    if alliance.is_at_war:
                                        self.user.profile.role = ALLIANCE_ROLE.RECRUIT

                                    else:
                                        self.user.profile.role = ALLIANCE_ROLE.REGULAR

                                    self.user.profile.save()

                                else:
                                    self.answer_command_data['error'] = ALLIANCE_ERROR.IS_AT_WAR

                            elif request_type == 'suggest':
                                alliance.requests.append(AllianceRequest(
                                    user_id=self.user.profile.id
                                ))

                                alliance.save()

                            alliance_invite.delete()

                        else:
                            print('An user tried to accept an unknown alliance invite from: {}'.format(sender_id))

                    else:
                        print('An user tried to accept an invite but already belong to any alliance: {}'.format(self.user.profile.id))

            else:
                self.answer_command_data['error'] = ALLIANCE_ERROR.ALLIANCE_IS_FULL

        else:
            self.answer_command_data['error'] = ALLIANCE_ERROR.ALLIANCE_DO_NOT_EXIST
