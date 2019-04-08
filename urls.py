
import tornado.web

from handlers.login_handler import LoginHandler
from handlers.ya_authorization_handler import YaAuthorizationHandler
from handlers.gallery_handler import GalleryHandler
from py_scripts.get_token_for_ya_disk import GetTokenForYaDisk
from handlers.make_like_handler import MakeLikeHandler

urls = [
    (r"/login/?", LoginHandler,),
    (r"/?", GalleryHandler,),
    (r"/ya_get_token/?", YaAuthorizationHandler,),
    (r"/get_token_for_ya_disk/?", GetTokenForYaDisk,),
    (r"/make_like_handler/?", MakeLikeHandler,),

    (r"/static/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static"}),
    (r"/src/(.*)/?", tornado.web.StaticFileHandler, {"path": "./static/src"},),
]
