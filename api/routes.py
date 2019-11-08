from aiohttp import web
from .controller import *
from .auth import *


def setup_routes(app):
    routes = [
        web.route('GET', '/test', test_controller),
        web.route('GET', '/auth', auth),
        web.route('GET', '/login', login_handler),
        web.route('GET', '/signup', signup_handler),
        web.route('GET', '/getuser', getuser_handler),
    ]
    app.add_routes(routes)
