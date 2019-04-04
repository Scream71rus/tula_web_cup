
from handlers.base_handler import BaseHandler


class LoginHandler(BaseHandler):
    async def get(self):
        self.write('qwe')