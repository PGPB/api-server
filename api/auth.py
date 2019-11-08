from aiohttp import web
from time import time
import jwt
import json

from .model import *

__all__ = ('login_handler', 'permits', 'logout_handler', 'signup_handler', 'getuser_handler', )

access_lives = 600
refresh_lives = 3600


async def login_handler(request):
    """ Authentication: Return tokens if credentials are right """
    login = request.query.get('login')
    password = request.query.get('password')

    user = await get_user_by_credentials(login, password)
    if user:
        tokens = create_tokens(request.config_dict['secret_key'], user['_id'], user['status'])
        return web.json_response(tokens)
    return web.HTTPBadRequest(text='Incorrect login or password')


async def logout_handler(request):
    ...


async def signup_handler(request):
    """" Registration: Return user_id """
    try:
        if not request.has_body:
            raise Exception('No data provided')
        data = await request.json()
        result = await create_user(data)
        return web.json_response({'user_id': result}, status=201)
    except Exception as e:
        return web.Response(text=str(e), status=400)


async def getuser_handler(request):
    # not working
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
    """ Return dict with access token """
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
    response = {'access_token': access_encoded}  # , 'refresh_token': refresh_encoded}
    return response


def is_token_valid(payload):
    if payload['expires'] < time():
        raise web.HTTPUnauthorized(text='Token expired')
