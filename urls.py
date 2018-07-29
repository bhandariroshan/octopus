import tornado.ioloop
import tornado.web as web
from views import MainHandler, WordCloudHandler, LogInHandler, AdminHandler, LogOutHandler
from settings import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base as models_base # get the declared sqlalchemy base

db_engine = create_engine(options.db_connection_str) # setup db engine for sqlalchemy
db_session = sessionmaker() # setup the session maker for sqlalchemy


class MyApplication(web.Application):
    """ Inhierited tornado.web.Application - stowing some sqlalchemy session information in the application """

    def __init__(self, settings, handlers, session):
        """ setup the session to engine linkage in the initialization """
        self.session = session
        self.session.configure(bind=db_engine)
        super(MyApplication, self).__init__(handlers=handlers, settings=settings, session=self.session)

    def create_database(self):
        """

        :return:
        """

        models_base.metadata.create_all(db_engine)


def make_app():
    handlers = [
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': 'static'}),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
        (r"/", MainHandler),
        (r"/cloud", WordCloudHandler, dict(db_session=db_session)),
        (r"/login", LogInHandler),
        (r"/logout", LogOutHandler),
        (r"/admin", AdminHandler, dict(db_session=db_session)),

    ]

    settings = {
        "cookie_secret": "roshan",
        "login_url": "/login"
    }

    application = MyApplication(handlers=handlers, settings=settings, session=db_session)
    return application