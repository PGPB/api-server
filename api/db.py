from mongoengine import *
from datetime import datetime

connect('testmongoengine')


class User(Document):
    login = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    first_name = StringField(required=True)
    middle_name = StringField()
    last_name = StringField(required=True)
    status = IntField(required=True, default=0)
