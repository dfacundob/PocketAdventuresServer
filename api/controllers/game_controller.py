import zlib
import json
import base64

from flask import request

from command.game_command.login_command import LoginHandler
from api.command_handler import handle_game_command_list, add_command_answer
from utils.utils import get_signature


def game_route(user):
    if int(request.form['czlb']):
        # Skip the 4 first bytes since it's the length
        decompressed_data = zlib.decompress(base64.b64decode(request.form['data'])[4:])
        user_post_data = json.loads(decompressed_data)

    else:
        user_post_data = json.loads(request.form['data'])

    payload = {}

    payload['service'] = 'GamePacket'

    # if set to true (1) the game will decompress our data field with base64 + zlib
    payload['czlb'] = 1
    payload['chk'] = 0

    data = {}

    data['packetCount'] = 0
    data['list'] = []

    if get_signature(request.form, user.token, 'vm51OOMgm8uFrQxjYZTJ') == request.form['sig']:
        if user_post_data['packetType'] == 'login':
            add_command_answer(
                LoginHandler,
                'logOK',
                user_post_data['packetData'],
                data['list'],
                user
            )

        elif user_post_data['packetType'] == 'cmdList':
            data['packetCount'] = user_post_data['packetData']['packetCount']
            handle_game_command_list(
                user_post_data['packetData']['cmdList'], data['list'], user)

    else:
        if user_post_data['packetType'] == 'cmdList':
            data['packetCount'] = user_post_data['packetData']['packetCount']

        data['list'].append({'cmdName': 'logOut', 'cmdData': {}})

    data = json.dumps(data).encode('utf-8')
    compressed = len(data).to_bytes(4, 'big') + zlib.compress(data)
    compressed = base64.b64encode(compressed).decode('utf-8')

    payload['data'] = compressed
    return json.dumps(payload)
