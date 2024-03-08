from flask import Blueprint
from api.controllers import controllers


routes = Blueprint('api', __name__)

for controller in controllers:
    view_func_decorator = controller.get("decorator")

    if view_func_decorator is not None:
        view_func = view_func_decorator(controller['view_func'])

    else:
        view_func = controller['view_func']

    routes.add_url_rule(
        controller['rule'],
        view_func=view_func,
        methods=['POST']
    )
