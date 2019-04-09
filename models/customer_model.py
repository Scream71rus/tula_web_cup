

class CustomerModel:
    async def save_customer_ya_token(self, data):
        sql = """insert into twc.customer(first_name, last_name, display_name, default_email, 
                                          client_id, login, expires_in, access_token, refresh_token) 
                 values(%(first_name)s, %(last_name)s, %(display_name)s, %(default_email)s, 
                        %(client_id)s, %(login)s, %(expires_in)s, %(access_token)s, %(refresh_token)s)
                 returning id"""

        cursor = await self.db.execute(sql, data)
        return cursor.fetchone().get('id')

    async def update_customer_ya_token(self, expires_in, access_token, refresh_token, customer_id):
        sql = """update twc.customer set expires_in=%(expires_in)s, 
                                         access_token=%(access_token)s,
                                         refresh_token=%(refresh_token)s where id = %(customer_id)s"""

        await self.db.execute(sql, {'expires_in': expires_in,
                                    'access_token': access_token,
                                    'refresh_token': refresh_token,
                                    'customer_id': customer_id})

    async def check_customer(self, default_email):
        sql = """select * from twc.customer where default_email = %s"""
        cursor = await self.db.execute(sql, (default_email,))
        return cursor.fetchone()

    async def set_customer_cookie(self, cookie, customer_id):
        sql = """insert into twc.cookie(cookie, customer_id) values(%s, %s)"""
        await self.db.execute(sql, (cookie, customer_id,))

    async def get_customer_by_cookie(self, cookie):
        try:
            sql = """select customer_id from twc.cookie where cookie = %s"""
            cursor_cookie = await self.db.execute(sql, (cookie,))

            sql = """select * from twc.customer where id = %s"""
            cursor = await self.db.execute(sql, (cursor_cookie.fetchone().get('customer_id'),))
            return cursor.fetchone()
        except Exception as ex:
            print(ex)
            return None

    async def delete_customer_cookie(self, cookie):
        sql = """delete from twc.cookie where cookie = %s"""
        await self.db.execute(sql, (cookie,))
