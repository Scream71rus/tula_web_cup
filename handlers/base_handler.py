
import tornado.web

from models.customer_model import CustomerModel


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    # TODO добавить проверку на пользователя

    # @property
    # def customer(self):
    #     return self._customer
    #
    # async def prepare(self):
    #     self._session_key = self.get_cookie("twc_cookie", None)
    #     self._customer = yield self.get_customer_by_customer_id(customer_id)
