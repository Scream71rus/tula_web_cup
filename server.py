
import sys
import os

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import logging
import asyncio
import tornado.ioloop
import tornado.log
import tornado.platform.asyncio

from tornado.options import define, options, parse_config_file

from django.conf import settings
settings.configure()

from application import Application

import urls


if __name__ == '__main__':
    define("port", type=int)
    define("debug", type=bool)
    define("template_path", type=str)
    define("dsn", type=str)
    define("size_db_connection_pool", type=int)

    define("ya_app_id", type=str)
    define("ya_app_pass", type=str)

    define("ya_disk_id", type=str)
    define("ya_disk_pass", type=str)
    define("ya_disk_expires_in", type=str)
    define("ya_disk_access_token", type=str)
    define("ya_disk_refresh_token", type=str)
    define("ya_disk_public_url", type=str)
    define("ya_disk_public_key", type=str)

    parse_config_file("application.conf")

    if options.debug == "yes":
        tornado.log.app_log.setLevel(logging.DEBUG)
    elif options.debug == "no":
        tornado.log.app_log.setLevel(logging.INFO)

    # tornado.ioloop.IOLoop.instance()
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    application = Application(
        urls.urls,
        template_path=options.template_path,
        debug=(True if options.debug == "yes" else False))

    application.listen(options.port)

    # tornado.ioloop.IOLoop.current().start()
    asyncio.get_event_loop().run_forever()
