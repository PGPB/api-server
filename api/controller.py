from aiohttp import web
from aiohttp_session import get_session
import jwt

from .auth import permits
from .model import *


async def auth(request):
    permits(request, 'read')
    return web.HTTPOk()
