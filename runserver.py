from urls import *


if __name__ == "__main__": # main
    application = make_app()
    # application.create_database() # create the database
    application.listen(8888) # listen on the right port
    print('Web server running, Listening on port 8888')
    tornado.ioloop.IOLoop.instance().start() # startup ioloop