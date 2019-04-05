
import tornado.web

from handlers.login_handler import LoginHandler


urls = [
    (r"/static/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static"}),
    (r"/src/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static/src"},),

    (r"/login/?", LoginHandler,),
]

# urls.extend(handlers.city_target_shop.urls)
