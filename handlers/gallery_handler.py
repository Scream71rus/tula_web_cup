
import json
import urllib.parse
import math

from tornado import httpclient
from tornado.options import options

from handlers.base_handler import BaseHandler
from models.customer_model import CustomerModel
from models.img_model import ImgModel


class GalleryHandler(BaseHandler, CustomerModel, ImgModel):
    async def get_total_img(self):
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
        public_key = {'public_key': options.ya_disk_public_key}
        url = url + urllib.parse.urlencode(public_key) + '&'
        url = url + 'limit=1'

        http_client = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url, method='GET')
        responce = await http_client.fetch(request)

        data_json = responce.body
        data = json.loads(data_json)
        embedded = data.get('_embedded')

        return embedded.get('total')

    async def get(self):
        cookie = self.get_cookie("twc_cookie", None)
        if cookie:
            customer = await self.get_customer_by_cookie(cookie)
        else:
            customer = None

        total_img = await self.get_total_img()

        count_img = int(self.get_argument('count_img', 10))
        page_number = int(self.get_argument('page_number', 0))

        public_key = {'public_key': options.ya_disk_public_key}

        url = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
        url = url + urllib.parse.urlencode(public_key) + '&'

        if count_img == 0:
            url = url + 'limit={}'.format(total_img) + '&'
        else:
            url = url + 'limit={}'.format(count_img) + '&'

        url = url + 'offset={}'.format(count_img * page_number) + '&'
        url = url + 'sort=name'

        http_client = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url, method='GET')
        responce = await http_client.fetch(request)

        data_json = responce.body
        data = json.loads(data_json)
        embedded = data.get('_embedded')
        items = embedded.get('items')
        images = []
        for item in items:
            resource_id = item.get('resource_id')
            name = item.get('name')
            preview = item.get('preview')
            file = item.get('file')

            data = {
                'name': name,
                'preview': preview,
                'file': file,
                'like': None,
                'resource_id': resource_id
            }
            if customer:
                like = await self.check_like(customer.get('id'), resource_id)
                data['like'] = like

            images.append(data)

        if count_img != 0:
            pages = math.ceil(total_img/count_img)
        else:
            pages = 1
        self.render('gallery.html', images=images, pages=pages,
                    count_img=count_img, customer=customer, page_number=page_number)

    async def post(self):
        cookie = self.get_cookie("twc_cookie", None)
        if cookie:
            customer = await self.get_customer_by_cookie(cookie)
        else:
            customer = None

        if customer:
            like_img = self.get_argument("like_img")
            like_img = like_img == "True"

            resource_id = self.get_argument("resource_id")
            data = {
                'like_img': like_img,
                'resource_id': resource_id,
                'customer_id': customer.get('id')
            }
            like = await self.check_like(data.get('customer_id'), data.get('resource_id'))
            if like is not None:
                await self.update_like(data)
            else:
                await self.set_img_like(data)

        self.redirect('/')
