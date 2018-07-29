from tornado.web import RequestHandler
import urllib.request
from utilities.html_utilities import HTMLUtilities
from utilities.word_counter import WordCounter
from utilities.async_encryptor import AsyncEncryptor
from tornado_sqlalchemy import SessionMixin
from tornado import web, gen
from models import WordManager, Words
import json
import requests
privatekey = None


class LogOutHandler(RequestHandler):
    """ Handle Logout. """
    def get_current_user(self):
        """

        :return:
        """

        return self.get_cookie("username")

    def get(self):
        """

        :return:
        """

        self.set_cookie("username", '')
        self.redirect('/login')


class LogInHandler(RequestHandler):
    template = "templates/login.html"

    def get_current_user(self):
        """

        :return:
        """
        ''' Login request is based on cookie. Return if any user is set on cookie. '''
        return self.get_cookie("username")

    def get(self):
        """

        :return:
        """
        ''' Handle Login request. '''
        items = []

        if self.get_current_user():
            self.redirect('/admin')
            return
        self.render(self.template, title="Login Page", items=items)

    def post(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        ''' Verify if username and password is accurate, redirect to admin page if active. '''

        data = self.request.arguments
        try:
            username = str(data['username'][0].decode("utf-8"))
        except:
            username = ''

        try:
            password = str(data['password'][0].decode("utf-8"))
        except:
            password = ''

        if username == 'octopus' and password == 'octopus123':
            self.set_cookie("username", self.get_argument("username"))
            self.redirect("/admin")
        else:
            pass


class AdminHandler(RequestHandler, SessionMixin):
    template = "templates/admin.html"

    def initialize(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        ''' WordCloudHandler.initialize - Setup the Models we will need for this handler '''

        db_session = kwargs.pop('db_session')
        self.manager = WordManager(db_session=db_session)

    def get_current_user(self):
        """

        :return:
        """
        ''' return current user. '''
        return self.get_cookie("username")

    def get(self):
        """

        :return:
        """
        ''' Handle admin page request. '''
        items = []
        data = self.manager.get_all_data()
        global privatekey
        for each_data in data:
            each_data = json.loads(each_data)
            new_dict = {
                'word': AsyncEncryptor.decrypt_message(each_data['encryptedword'], privatekey),
                'count': each_data['frequency']
            }
            items.append(new_dict)

        if not self.get_current_user():
            self.redirect('/login')
            return

        if not privatekey:
            self.redirect('/')
            return

        self.render(self.template, title="Admin Page", items=items)


class MainHandler(RequestHandler):
    template = "templates/main.html"

    def get(self):
        """

        :return:
        """
        ''' Handle main request page, i.e page to enter url for cloud formation. '''

        items = []
        self.render(self.template, title="Home Page", items=items)


class WordCloudHandler(RequestHandler, SessionMixin):
    template = "templates/cloud.html"

    def initialize(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

        """ WordCloudHandler.initialize - Setup the Models we will need for this handler """

        db_session = kwargs.pop('db_session')
        self.manager = WordManager(db_session=db_session)

    def save_words(self, word_list):
        """

        :param word_list:
        :return:
        """
        ''' Save encrypted and hashed words in database. '''
        for each_word in word_list:
            word = Words(
                saltedhash=each_word['saltedhash'],
                encryptedword=each_word['encryptedword'],
                frequency=each_word['size']
            )  # populate an ORM with it
            # done = yield gen.Task(self.manager.create_or_update, word)  # do the create, wait for it to finish
            self.manager.create_or_update(word)

    @web.asynchronous  # this will be async
    @gen.coroutine  # we will be using coroutine, with gen.Task
    def get(self):
        """

        :return:
        """
        ''' Do no allow get request. '''
        self.redirect('/')
        return

    @web.asynchronous  # this will be async
    @gen.coroutine  # we will be using coroutine, with gen.Task
    def post(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        ''' Handle post request, render word cloud.'''
        utility = HTMLUtilities()

        # get post data from request
        data = self.request.arguments
        try:
            url_string = str(data['urlstring'][0].decode("utf-8"))
        except:
            url_string = ''

        if 'http://' not in url_string and 'https://' not in url_string:
            url_string = 'http://' + url_string

        try:
            html = requests.get(url_string).text
        except:
            try:
                print('URL STRING IS::: ', url_string)
                url_string = url_string.replace('http://', 'https://')
                html = requests.get(url_string).text
            except:
                self.redirect('/')
                return

        text = utility.text_from_html(html)

        # send text of the web page to get word count, hash of words
        word_count_list, private_key, data_list_for_template = WordCounter.get_sorted_and_hashed_word_count_list(text=text, url=url_string)
        self.save_words(word_list=word_count_list)

        # save private key for latter decryption
        global privatekey
        privatekey = private_key

        self.render(self.template, title="Word Cloud", data=json.dumps({'data':data_list_for_template}))