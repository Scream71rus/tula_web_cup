
import sys
import os

sys.path.append(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '.'))

import logging
import tornado.ioloop
import tornado.log
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

    parse_config_file("application.conf")

    if options.debug == "yes":
        tornado.log.app_log.setLevel(logging.DEBUG)
    elif options.debug == "no":
        tornado.log.app_log.setLevel(logging.INFO)

    tornado.ioloop.IOLoop.instance()

    application = Application(
        urls.urls,
        template_path=options.template_path,
        debug=(True if options.debug == "yes" else False))

    application.listen(options.port)

    tornado.ioloop.IOLoop.current().start()
