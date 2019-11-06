from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient

from .routes import setup_routes

__all__ = ('create_app',)


def create_app(config: dict):
    app = web.Application()
    app['config'] = config
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    setup_routes(app)

    return app


async def on_start(app):
    try:
        app['db_conn'] = AsyncIOMotorClient(app['config']['DB_URL'])
        app['db'] = app['db_conn']
        print('DB connecting')
    except Exception as e:
        print('There are some problems with DB connection')


async def on_shutdown(app):
    try:
        app['db_conn'].close()
        print('DB closed')
    except Exception as e:
        print('Error in closing DB connection')
