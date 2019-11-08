from time import time
start = time()
from ast import literal_eval
import pprint
from mongoengine import *

connect('testmongoengine')


class User(Document):
    login = StringField(required=True)
    password = StringField(required=True)


# for i in range(1000, 2000):
#     user = User(login='user'+str(i), password='pswd'+str(i)).save()
# for user in User.objects:
#     data = literal_eval(user.to_json())
#     try:
#         pprint.pprint(data)
#     except KeyError:
#         print('no login')
# print(time() - start)