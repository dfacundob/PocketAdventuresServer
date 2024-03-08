from flask import request

from api.controllers.game_controller import game_route
from api.controllers.social_controller import social_route
from api.controllers.device_controller import device_route
from api.controllers.message_controller import message_route
from api.controllers.alliance_controller import alliance_route
from api.controllers.payments_controller import payments_route

from database.models.user.user import User


def get_user(f):
    ''' Decorator that return an instance of User model with a given uid '''
    def wrapper(*args, **kwargs):
        user_id = request.form['uid']

        user = User.query.get(user_id)

        if user is not None:
            return f(user, *args, **kwargs)

        else:
            print('An user tried to connect with an unknown uid: {}'.format(user_id))
            return ''

    wrapper.__name__ = f.__name__
    return wrapper


controllers = [
    {
        "rule": "/game",
        "view_func": game_route,
        "decorator": get_user
    },
    {
        "rule": "/social",
        "view_func": social_route,
        "decorator": get_user
    },
    {
        "rule": "/",
        "view_func": device_route
    },
    {
        "rule": "/sms",
        "view_func": message_route,
        "decorator": get_user
    },
    {
        "rule": "/alliance",
        "view_func": alliance_route,
        "decorator": get_user
    },
    {
        "rule": "/payments",
        "view_func": payments_route
    }
]
