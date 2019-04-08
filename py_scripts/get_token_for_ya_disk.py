
import json
import os
import urllib.parse

from tornado import httpclient
from tornado.options import options

from handlers.base_handler import BaseHandler
from models.customer_model import CustomerModel


class GetTokenForYaDisk(BaseHandler, CustomerModel):
    async def get(self):
        auth_url = 'https://oauth.yandex.ru/authorize?'  # Яндекс.OAuth для пользователя
        auth_url = auth_url + 'response_type=code' + '&'  # требуемый ответ
        auth_url = auth_url + 'client_id={}'.format(options.ya_disk_id)  # id приложения
        auth_url = auth_url.replace(' ', '')

        self.redirect(auth_url)

    async def post(self):
        error = self.get_argument('error', None)
        if error is None:
            ya_code = self.get_argument('code', None)  # code для обмена на токен
            url = 'https://oauth.yandex.ru/token'

            disk_token = options.ya_disk_id
            disk_password = options.ya_disk_pass

            body = {"grant_type": "authorization_code",
                    "code": ya_code,
                    "client_id": disk_token,
                    "client_secret": disk_password
                    }
            body = urllib.parse.urlencode(body)

            http_client = httpclient.AsyncHTTPClient()
            request = httpclient.HTTPRequest(url, method='POST',
                                             headers={'Content-type': 'application/x-www-form-urlencoded',
                                                      'Host': 'oauth.yandex.ru'},
                                             body=body)

            responce = await http_client.fetch(request)

            json_data = responce.body
            ya_data = json.loads(json_data)

            data = {
                'expires_in': str(ya_data.get('expires_in')),
                'access_token': ya_data.get('access_token'),
                'refresh_token': ya_data.get('refresh_token'),
            }
