import asyncio
import pymongo.errors
from bson.json_util import dumps
from bson.objectid import ObjectId
import mongoengine

from .db import *


async def create_user(data):
    try:
        user = User(
            login=data['login'],
            password=data['password'],
            first_name=data['first_name'],
            middle_name=data['middle_name'],
            last_name=data['last_name']
        ).save()
        return str(user.pk)
    except mongoengine.errors.NotUniqueError:
        raise Exception('Login has occupied already')
    except KeyError as e:
        raise Exception(f'{e} field is not provided')


async def get_user_by_credentials(login, password):
    user = User.objects(login=login, password=password).first()
    ...