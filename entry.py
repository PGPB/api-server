import asyncio

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import base64
from cryptography import fernet

import api
import api.settings

cookie_key = fernet.Fernet.generate_key()
cookie_secret_key = base64.urlsafe_b64decode(cookie_key)
app_secret_key = cookie_key.decode('UTF-8')

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("uvloop is not available")

app = web.Application(middlewares=[
    session_middleware(EncryptedCookieStorage(cookie_secret_key))
])
app['secret_key'] = str(app_secret_key)
api_app = api.create_app(config=api.settings.load_config())

app.add_subapp('/api', api_app)

if __name__ == '__main__':
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain('fullchain.pem', 'privkey.pem')
    web.run_app(app, host='0.0.0.0', port=5000)
