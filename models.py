from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from tornado.concurrent import return_future, run_on_executor
from tornado.ioloop import IOLoop
from tornado.options import options
from concurrent.futures import ThreadPoolExecutor
import json
from settings import *
import _mysql_exceptions

Base = declarative_base() # declaritive base for sqlalchemy
EXECUTOR = ThreadPoolExecutor(options.executor_max_threads) # setup global executor

'''
    This class handles database connection and operations.
    We define ORM layer using SQL alchemy, for CRUD operations on database.
    
'''

class Words(Base):
    __tablename__ = 'words'

    saltedhash = Column(String(1000), primary_key=True)
    encryptedword = Column(String(1000))
    frequency = Column(BigInteger,default=0)

    def to_json(self): # hrm, serializing to_json
        return(json.dumps({'saltedhash': self.saltedhash, 'encryptedword':self.encryptedword, 'frequency': self.frequency})) #indeed


class WordManager(object):
    def __init__(self, db_session, io_loop=None, executor=EXECUTOR): # initial setup as an executor
        """

        :param db_session:
        :param io_loop:
        :param executor:
        """

        ''' Manager class for model initialization. '''

        self.io_loop = io_loop or IOLoop.instance() # grabe the ioloop or the global instance
        self.executor = executor # grab the executor
        self.db_session = db_session # get the session

    # @run_on_executor  # okay, run this method on the instance's executor
    # @return_future  # return a future
    def get_all_data(self, callback=None):
        """

        :param callback:
        :return:
        """

        ''' Return all data from database. '''

        session = self.db_session() # setup the session in this thread
        result = None
        try:
            result = session.query(Words).filter()# do the request
            result_data = []
            for each_result in result:
                result_data.append(each_result.to_json())
            session.close() # close the session
            return result_data
        except Exception as e:
            result = e
            session.close()

    # @run_on_executor  # okay, run this method on the instance's executor
    # @return_future  # return a future
    def create_or_update(self, word, callback=None):
        """

        :param word:
        :param callback:
        :return:
        """

        """ Create or update data in the database. """

        session = self.db_session() # setup session in this thread
        success = True
        try:
            session.add(word) # add the orm to session
            session.commit() # commit the session when added
        except Exception as e: # if there is an exception
            try:
                word = session.query().filter(Words.saltedhash==word.saltedhash)

                if word.has_member_entities:
                    word.encryptedword = word.encryptedword
                    word.frequency = word.frequency
                session.commit()

            except Exception as e:
                session.rollback()
                success = e  # return that it failed
            session.close()  # close the session