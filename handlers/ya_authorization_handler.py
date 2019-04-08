
import json
import os
import urllib.parse

from tornado import httpclient
from tornado.options import options

from handlers.base_handler import BaseHandler
from models.customer_model import CustomerModel


class YaAuthorizationHandler(BaseHandler, CustomerModel):
    async def get(self):
        error = self.get_argument('error', None)
        if error is None:
            ya_code = self.get_argument('code', None)  # code для обмена на токен
            url = 'https://oauth.yandex.ru/token'

            app_token = options.ya_app_id
            app_password = options.ya_app_pass

            body = {"grant_type": "authorization_code",
                    "code": ya_code,
                    "client_id": app_token,
                    "client_secret": app_password
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

            http_client = httpclient.AsyncHTTPClient()

            request = httpclient.HTTPRequest('https://login.yandex.ru/info?', method='GET',
                                             headers={'Authorization': 'OAuth ' + data.get('access_token')})

            responce = await http_client.fetch(request)

            data_json = responce.body
            customer_info = json.loads(data_json)

            data['first_name'] = customer_info.get('first_name')
            data['last_name'] = customer_info.get('last_name')
            data['display_name'] = customer_info.get('display_name')
            data['default_email'] = customer_info.get('default_email')
            data['client_id'] = customer_info.get('client_id')
            data['login'] = customer_info.get('login')

            customer = await self.check_customer(data.get('default_email'))

            if customer is None:
                customer_id = await self.save_customer_ya_token(data)
                session_key = os.urandom(24).hex()
                self.set_cookie('twc_cookie', session_key, expires_days=180)
                await self.set_customer_cookie(session_key, customer_id)
            else:
                await self.update_customer_ya_token(data.get('expires_in'),
                                                    data.get('access_token'),
                                                    data.get('refresh_token'),
                                                    customer.get('id'))

                session_key = os.urandom(24).hex()
                self.set_cookie('twc_cookie', session_key, expires_days=180)
                await self.set_customer_cookie(session_key, customer.get('id'))

            self.redirect('/')
        else:
            self.redirect('/login')