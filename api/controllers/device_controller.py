import json
import secrets

from uuid import uuid4
from datetime import datetime, timedelta

from flask import request
from database.models.user.user import User


def device_route():
    user_data = json.loads(request.form['data'])

    if user_data['action'] == 'aauth':
        # mean that we have a new user
        print('Creating new user in database')

        user = User(
            user_id=str(uuid4()),
            unique_identifier=user_data['unique_identifier'],
            locale=user_data['locale']
        ).save()

        print('New user created with uid {}'.format(user.user_id))

    else:
        user = User.query.filter_by(user_id=user_data['user_id']).first()

        if user is None:
            print('An user tried to connect with an unknown user_id: {}'.format(user_data['user_id']))
            return ''

        if user.is_banned or user.is_emulated:
            return ''

        if user.emulated_user_id is not None:
            if user.emulation_start_date + timedelta(minutes=30) > datetime.utcnow():
                emulated_user = User.query.filter_by(user_id=user.emulated_user_id).first()

                if emulated_user is None:
                    print('An user tried to emulate an unknown user')
                    return ''

                if not emulated_user.is_emulated:
                    # Means the emulation got stopped
                    user.emulated_user_id = None
                    user.emulation_start_date = None

                else:
                    user = emulated_user

            else:
                # Means the emulation is finished
                user.emulated_user_id = None
                user.emulation_start_date = None

        print('{} connected !'.format(user.user_id))

    user.token = secrets.token_urlsafe(16)
    user.last_command_count = -1
    user.save()

    payload = {}

    payload['uid'] = user.id
    payload['forced'] = 0
    payload['userId'] = user.user_id
    payload['code'] = user.profile.friend_code
    payload['token'] = user.token
    payload['mb'] = ''
    payload['czlb'] = 1

    return json.dumps(payload)
