import os
import tornado

from pony.orm import db_session

from redsparrow.orm import User, Thesis
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
        user = User.select(lambda u: u.login == login and u.email == email)[:]
        if len(user) > 0:
            return self.error(code=-32602, message='User with email %s already exists' % email)
        user = User(login=login, password=password, email=email, name=name, surname=surname)
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
            self.success(user[0].to_dict(with_collections=True, related_objects=True))
            return
        self.error(message='User not found')

    def test_method(self):
        """ Ping method. It tests if server is up."""
        self.success(message='OK')

class Thesis(BaseMethod):

    def __init__(self):
        super(Login, self).__init__('thesis')

    @db_session
    def run_analysis(self, thesis_id):
        """
            run_analysis method get Thesis by thesis_id and process on it PlagiarismDetector

            :param thesis_id: id of thesis to analysis

        """
        thesis = Thesis.select(lambda t: t.id == thesis_id)[:]
        if len(thesis) == 0:
            return self.error(message="Thesis not found")
        detector = PlagiarismDetector()
        result = detector.process(thesis[0].to_dict(with_collections=True, relate_object=True))
        self.success(result)




