import asyncio
import pymongo.errors
from bson.json_util import dumps
from bson.objectid import ObjectId


class User:
    @staticmethod
    async def create(db, data):
        result = await db.users.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    async def get(db, id):
        result = await db.users.find_one({'_id': ObjectId(id)}, {'login': 1, 'access': 1})
        if result:
            result['_id'] = str(result['_id'])
            return result
        return {'status': 'not found'}

    @staticmethod
    async def credentials(db, login, password):
        result = await db.users.find_one({'login': login, 'password': password}, {'login': 1, 'access': 1})
        if result:
            result['_id'] = str(result['_id'])
            return result
        return False


