import asyncio
from aiohttp import web
# import ssl

import api
import api.settings


try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print("uvloop is not available")

app = web.Application()
api_app = api.create_app(config=api.settings.load_config())
app.add_subapp('/api', api_app)

if __name__ == '__main__':
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.load_cert_chain('fullchain.pem', 'privkey.pem')
    web.run_app(app, host='0.0.0.0', port=5000)
