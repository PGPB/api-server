# from aiohttp import web
from .controller import *


def setup_routes(app):
    routes = [
        web.route('GET', '/test', test_controller),

    ]
    app.add_routes(routes)
