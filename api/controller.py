from aiohttp import web
import jwt

from .auth import permits
# from aiohttp_security import (remember, forget, authorized_userid,
#                               check_authorized, check_permission
#                               )
from aiohttp_session import get_session
from .model import *


async def test_controller(request):
    session = await get_session(request)
    session['hello'] = ''
    print(session)
    return web.HTTPOk()


async def auth(request):
    permits(request, 'read')
    return web.HTTPOk()
    # print(request.headers['Accept'])
    # print(type(request.headers['Accept']))
    # got_token = request.query['token']
    # decoded = jwt.decode(got_token, key, algorithms=['HS256'])
    # # print(decoded)
    # return web.HTTPUnauthorized()


