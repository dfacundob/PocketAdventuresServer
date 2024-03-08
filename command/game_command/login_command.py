from datetime import datetime
from command.base_command import BaseCommand


class LoginHandler(BaseCommand):

    def answer(self):
        self.answer_command_data['version'] = '1.22.1'
        self.answer_command_data['sync'] = 1
        self.answer_command_data['userId'] = self.user.id
        self.answer_command_data['token'] = self.user.token

        self.answer_command_data['myAccountIsLocked'] = self.user.profile.is_under_attack
        self.answer_command_data['tutorialCompleted'] = self.user.profile.is_tutorial_completed  # Switch that to 1 if you don't want the intro to start
        self.answer_command_data['levelBasedOnScore'] = self.user.profile.level_based_on_score
        self.answer_command_data['currentTimeMillis'] = str(int(datetime.utcnow().timestamp() * 1000))
        self.answer_command_data['timeFromLastLogin'] = int((datetime.utcnow() - self.user.profile.last_login_time).total_seconds() * 1000)
        self.answer_command_data['timeFromLastUpdate'] = 0
        self.answer_command_data['androidPublicKey'] = 'someuselesskey'
        self.answer_command_data['androidGCMRegistrationID'] = ''
        self.answer_command_data['androidGCMRegistrationLastVersion'] = '1.7.0'
        self.answer_command_data['androidGPlayMainPassword'] = 'apassword'
        self.answer_command_data['androidGPlayPatchPassword'] = 'apassword'
        self.answer_command_data['services'] = {}

        if not self.user.profile.is_under_attack:
            self.user.last_command_time = datetime.utcnow()

        self.user.profile.last_login_time = datetime.utcnow()
        self.user.profile.save()
