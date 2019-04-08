
import tornado.web

from models.customer_model import CustomerModel


class BaseHandler(tornado.web.RequestHandler, CustomerModel):

    @property
    def db(self):
        return self.application.db

    @property
    def customer(self):
        return self._customer

    async def prepare(self):
        self._session_key = self.get_cookie("twc_cookie", None)
        if self._session_key:
            self._customer = await self.get_customer_by_cookie(self._session_key)
        else:
            self._customer = None