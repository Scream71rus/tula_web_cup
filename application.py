
import momoko
import psycopg2.extras
import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.options import options


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

        self._db = momoko.Pool(
            dsn=options.dsn,
            size=options.size_db_connection_pool,
            ioloop=tornado.ioloop.IOLoop.current(),
            cursor_factory=psycopg2.extras.DictCursor)

        self._db.connect()


    @property
    def db(self):
        return self._db
