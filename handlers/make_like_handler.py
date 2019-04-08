
from handlers.base_handler import BaseHandler
from models.img_model import ImgModel


class MakeLikeHandler(BaseHandler, ImgModel):
    async def post(self):
        if self.customer:
            like_img = self.get_argument("like_img")
            like_img = like_img == "True"

            resource_id = self.get_argument("resource_id")
            data = {
                'like_img': like_img,
                'resource_id': resource_id,
                'customer_id': self.customer.get('id')
            }
            like = await self.check_like(data.get('customer_id'), data.get('resource_id'))
            if like is not None:
                await self.update_like(data)
            else:
                await self.set_img_like(data)

        self.redirect('/')