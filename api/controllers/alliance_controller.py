import json

from flask import request

from api.command_handler import handle_command
from utils.utils import get_signature


def alliance_route(user):
    user_post_data = json.loads(request.form['data'])

    if get_signature(request.form, user.token, 'vm51OOMgm8uFrQxjYZTJ') == request.form['sig']:
        payload = {}
        data = {}

        handle_command(user_post_data['action'], user_post_data, data, 'action', user)

        if data.get('response_code') is None:
            payload['data'] = json.dumps(data)

        return json.dumps(payload)

    else:
        return ''
