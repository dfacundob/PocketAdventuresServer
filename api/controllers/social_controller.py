import json

from flask import request
from api.command_handler import handle_command
from utils.utils import get_signature


def social_route(user):
    user_post_data = json.loads(request.form['command'])

    if get_signature(request.form, user.token, '12a471bf6057ff00') == request.form['sig']:
        payload = {}
        payload['status'] = 'OK'

        handle_command(user_post_data['command'], user_post_data, payload, 'command', user)

        return json.dumps(payload)

    else:
        return ''
