
import tornado.web

from handlers.login_handler import LoginHandler


urls = [
    (r"/customer/static/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static"}),
    (r"/customer/src/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static/src"},),

    (r"/login/?", LoginHandler,),
]

# urls.extend(handlers.city_target_shop.urls)
