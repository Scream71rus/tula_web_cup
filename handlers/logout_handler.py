

from handlers.base_handler import BaseHandler


class LogOutHandler(BaseHandler):
    async def get(self):
        session_key = self.get_cookie("twc_cookie")
        await self.delete_customer_cookie(self._session_key)
        self.set_cookie("twc_cookie", '')
        self.redirect('/')