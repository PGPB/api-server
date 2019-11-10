from aiohttp import web
from time import time
import jwt
import json
import yaml
from pathlib import Path

from .model import *

__all__ = ('login_handler', 'permits', 'logout_handler', 'signup_handler', 'getuser_handler', )


async def login_handler(request):
    """ Authentication: Return tokens if credentials are right """
    login = request.query.get('login')
    password = request.query.get('password')

    user = await get_user_by_credentials(login, password)
    if user:
        tokens = create_tokens(config['JWT_KEY'], user['_id'], user['status'], config['JWT_ALGORITHM'])
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
    """" Raise exception if required permission is more than user permission """
    token = request.headers.get('Authorization')
    if not token:
        raise web.HTTPUnauthorized(text='Token is not provided')

    try:
        payload = jwt.decode(token, config['JWT_KEY'], algorithms=[config['JWT_ALGORITHM']])
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        raise web.HTTPUnauthorized(text='Invalid token')

    is_token_valid(payload)
    if permission > payload['access']:
        raise web.HTTPForbidden()


#
def create_tokens(key, user_id, access: int, algorithm) -> dict:
    """ Return access and refresh tokens """
    access_payload = {
        'user_id': user_id,
        'expires': time() + config['ACCESS_LIVES'],
        'access': access
    }
    refresh_payload = {
        'user_id': user_id,
        'expires': time() + config['REFRESH_LIVES']
    }
    # save refreshToken
    access_encoded = jwt.encode(access_payload, key, algorithm).decode('UTF-8')
    refresh_encoded = jwt.encode(refresh_payload, key, algorithm).decode('UTF-8')
    response = {'access_token': access_encoded, 'refresh_token': refresh_encoded}
    return response


def is_token_valid(payload):
    if payload['expires'] < time():
        raise web.HTTPUnauthorized(text='Token expired')


def load_config():
    """ Load env variables """
    response = {}
    file_path = Path(__file__).parent / 'config.yaml'
    with open(file_path, 'r') as file:
        keys = yaml.safe_load(file)
    for key, value in keys.items():
        response[key] = value
    return response


config = load_config()
