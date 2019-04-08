

class ImgModel:
    async def set_img_like(self, data):
        sql = """insert into twc.img_like(resource_id, like_img, customer_id) 
                 values(%(resource_id)s, %(like_img)s, %(customer_id)s)"""
        await self.db.execute(sql, data)

    async def check_like(self, customer_id, resource_id):
        sql = """select like_img from twc.img_like where customer_id = %s and resource_id = %s"""
        cursor = await self.db.execute(sql, (customer_id, resource_id))
        result = cursor.fetchone()
        if result is not None:
            return result.get('like_img')
        else:
            return None

    async def update_like(self, data):
        sql = """update twc.img_like set like_img = %(like_img)s 
                 where customer_id = %(customer_id)s and resource_id = %(resource_id)s"""
        await self.db.execute(sql, data)
