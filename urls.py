
import tornado.web

from handlers.login_handler import LoginHandler
from handlers.ya_authorization_handler import YaAuthorizationHandler

urls = [
    (r"/login/?", LoginHandler,),
    (r"/ya_get_token/?", YaAuthorizationHandler,),

    (r"/static/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static"}),
    (r"/src/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static/src"},),
]

# urls.extend(handlers.city_target_shop.urls)
