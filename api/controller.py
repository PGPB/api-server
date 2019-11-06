from aiohttp import web
import jwt

from .model import *


def test_controller(request):
    return web.HTTPOk()
