import os
import tornado

from pony.orm import db_session

from redsparrow.model import User
from .base import BaseMethod

class Register(BaseMethod):

    def __init__(self):
        super(Register, self).__init__('register')

    @db_session
    def process(self, login, password, email, name, surname):
        """
            Register method

            params - dict

            :param login: user Login

            :param email: user email

            :param password: hash of user password

            :param surname: user surname

            :param name: user name

            :returns: If success returns all user data else return JSON-RPC error object
        """
        super(Register, self).process()
        user =  User.select(lambda u: u.login == login and u.email == email)[:]
        if len(user) > 0:
            return self.error(code=-32602, message='User with email %s already exists' % email)
        user =  User(login=login, password=password, email=email, name=name, surname=surname)
        self.success("User %s added to DB" % login)



class Login(BaseMethod):

    def __init__(self):
        super(Login, self).__init__('login')


    @db_session
    def process(self, login, password):
        """
            Login method

            :param login: user Login

            :param password: hash of password
        """
        super(Login, self).process()
        user = User.select(lambda u: u.login == login and u.password == password)[:]
        if len(user) > 0:
            self._response.result = user[0].to_dict(with_collections=True, related_objects=True)
            self.success()
            return
        self.error(message='User not found')

    def test_method(self):
        """ Test doc"""

        pass
