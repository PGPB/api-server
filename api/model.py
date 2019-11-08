from bson.objectid import ObjectId
import json
import mongoengine

from .db import *


async def create_user(data: dict) -> str:
    """ Insert new document to User collection and return document _id """
    try:
        user = User(
            login=data['login'],
            password=data['password'],
            first_name=data['first_name'],
            middle_name=data['middle_name'],
            last_name=data['last_name']
        ).save()
        return str(user.id)
    except mongoengine.errors.NotUniqueError:
        raise Exception('Login has occupied already')
    except KeyError as e:
        raise Exception(f'{e} field is not provided')


async def get_user_by_credentials(login, password):
    """ Return user id and his status or None if user don't exist"""
    user = User.objects(login=login, password=password).only('status').first()
    if user:
        return json.loads((user.to_json()))
    return None
