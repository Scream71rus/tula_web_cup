
import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    # @property
    # def customer(self):
    #     return self._customer
    #
    # async def prepare(self):
        # self.session_start()
        # self._session_key = self.get_cookie("c_session_key", None)
        # customer_id = self.application.cache.get('eric_kartman:%s' % (self._session_key,))
        # self._customer = yield self.get_customer_by_customer_id(customer_id)
