from aiohttp import web
from time import time
import jwt

from .model import *

__all__ = ('login_handler', 'permits', 'logout_handler', 'signup_handler', 'getuser_handler', )

access_lives = 600
refresh_lives = 3600


async def login_handler(request):
    login = request.query.get('login')
    password = request.query.get('password')

    user = await User.credentials(request.app['db'], login, password)
    if user:
        response = create_tokens(request.config_dict['secret_key'], user['login'], user['access'])
        return web.json_response(response)
    return web.HTTPUnauthorized()


async def logout_handler(request):
    ...


async def signup_handler(request):
    login = request.query.get('login')
    password = request.query.get('password')

    data = {'login': login, 'password': password, 'access': []}
    result = await User.create(request.app['db'], data)
    if result:
        return web.json_response({'user_id': result}, status=201)
    return web.json_response({'status': 'failed'}, status=500)


async def getuser_handler(request):
    id = request.query.get('id')
    result = await User.get(request.app['db'], id)
    return web.json_response(result)


def permits(request, permission):
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token, request.config_dict['secret_key'])
    except jwt.exceptions.InvalidSignatureError:
        raise web.HTTPUnauthorized()
    except jwt.exceptions.DecodeError:
        raise web.HTTPInternalServerError()

    is_token_valid(payload)
    if permission in payload['access']:
        return True
    raise web.HTTPForbidden()


#
def create_tokens(key, user, access):
    access_payload = {
        'user_id': user,
        'expires': time() + access_lives,
        'access': access
    }
    refresh_payload = {
        'user_id': user,
        'expires': time() + refresh_lives,
    }
    # save refreshToken
    access_encoded = jwt.encode(access_payload, key).decode('UTF-8')
    # refresh_encoded = jwt.encode(refresh_payload, key).decode('UTF-8')
    response = {'accessToken': access_encoded}  # , 'refreshToken': refresh_encoded}
    return response


def is_token_valid(payload):
    if payload['expires'] < time():
        raise web.HTTPUnauthorized(text='Token expired')
