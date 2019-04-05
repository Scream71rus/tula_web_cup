
from tornado.options import options

from handlers.base_handler import BaseHandler


class LoginHandler(BaseHandler):
    async def get(self):
        self.render('login.html')

    async def post(self):
        auth_url = 'https://oauth.yandex.ru/authorize?'  # Яндекс.OAuth для пользователя
        auth_url = auth_url + 'response_type=code' + '&'  # требуемый ответ
        auth_url = auth_url + 'client_id={}'.format(options.ya_app_id)  # id приложения
        auth_url = auth_url.replace(' ', '')

        self.redirect(auth_url)
