import os
import tornado

from pony.orm import db_session

from redsparrow.model import User
from .base import BaseMethod

class Register(BaseMethod):

    def __init__(self):
        super(Register, self).__init__('register')

    @db_session
    def _process(self, *args, **params):
        """
            Register method

            :param login: user Login

            :param email: user email

            :param password: hash of user password

            :param surname: user surname

            :param name: user name

            :returns: If success returns all user data else return JSON-RPC error object
        """
        user =  User.select(lambda u: u.login == params['login'] and u.email == params['email'])[:]
        if len(user) > 0:
            return self.error('User with email %s already exists' % params['email'])
        user =  User(login=params['login'], password=params['password'], email=params['email'], name=params['name'], surname=params['surname'])
        self._response.success = "User %s added to DB" % params['login']
        self.success()



class Login(BaseMethod):

    def __init__(self):
        super(Login, self).__init__('login')


    @db_session
    def _process(self, login, password):
        user =  User.select(lambda u: u.login == login and u.password == password)[:]
        if len(user) > 0:
            self._response.result = user[0].to_dict(with_collections=True, related_objects=True)
            self.success()
            return
        self.error('User not found')

    def test_method(self):

        pass
