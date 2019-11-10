from aiohttp import web

from .auth import permits
from .model import *


async def auth(request):
    permits(request, 0)
    return web.HTTPOk()
