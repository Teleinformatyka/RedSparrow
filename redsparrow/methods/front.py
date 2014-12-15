import os
import tornado

from pony.orm import db_session

from redsparrow.orm import User, Thesis, ThesisDetails, Keyword, Level, ThesisStatus, FieldOfStudy
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


class UserMethods(BaseMethod):
    # for user setters and getters

    @db_session
    def edit_user(self, columnName, value, userId):
        if len(User[userId]) > 0:
            d = {columnName : value}
            self.success(User[userId].set(**d))

    @db_session
    def get_user_by_id(self, userId):
        user = User.select(lambda u: u.id == userId)
        if len(user) > 0:
            self.success(user[0].to_dict(with_collections=True, related_objects=True))
        self.error("User not found")

    @db_session
    def delete_user(self, userId):
        if len(User[userId]) > 0:
            self.success(User[userId].delete())
        self.error("User not found")

    @db_session
    def add_user_level_by_user_id(self,userId, levelId):
        user = User.select(lambda u: u.id == userId)
        if len(user) > 0:
            user[0].levels.add(levelId)
            self.success()
        self.error("User not found")

    @db_session
    def set_user_password_by_user_id(self, userId, password):
        user = User.select(lambda u: u.id == userId)
        if len(user) > 0:
            user[0].password = password
            self.success()
        self.error("User not found")

    @db_session
    def set_email(self, value):
        if '@' not in value:
            raise Exception("This doesn't look like an email address.")
        self.email = value

    @db_session
    def get_list_of_users(self):
        users = User.select(u for u in User)[:]
        if len(users) > 0:
            fin = []
            for special in users:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")







class ThesisMethods(BaseMethod):
    @db_session
    def edit_thesis(self, columnName, value, thesisId):
        if len(Thesis[thesisId]) > 0:
            d = {columnName : value}
            self.success(Thesis[thesisId].set(**d))

    @db_session
    def get_list_of_thesis(self):
        thesis = Thesis.select(t for t in Thesis)[:]
        if len(thesis) > 0:
            fin = []
            for special in thesis:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def delete_thesis(self, thesisId):
        if len(Thesis[thesisId]) > 0:
            self.success(Thesis[thesisId].delete())
        self.error("Thesis not found")

    @db_session
    def add_thesis_to_user_by_user_id(self, userId):
        self.users.add(userId)


    @db_session
    def get_thesis_by_title(self, query):
        thesis = Thesis.select(lambda t: t.thesis.equals(query))
        if len(thesis) > 0:
            self.success(thesis[0].to_dict(with_collections=True, related_objects=True))
        self.error("Thesis not found")

    @db_session
    def get_thesis_status_by_thesis_id(self, thesisId):
        if len(Thesis[thesisId]) > 0:
            self.success(Thesis[thesisId].thesisStatus)
        self.error("Thesis not found")

    @db_session
    def get_thesis_by_user_id(self, userId):
        thesis = Thesis.select(lambda t: t.thesis.users.contains(userId))
        if len(thesis) > 0:
            if len(thesis) > 1:
                fin = []
                for special in thesis:
                    fin.add(special.to_dict(with_collections=True, related_objects=True))
                self.success(fin)
            self.success(thesis.to_dict(with_collections=True, related_objects=True))
        self.error("Thesis not found")


    @db_session
    def get_thesis_status_by_title(self, thesisTitle):
        thesis = Thesis.select(lambda t: t.thesis.equals(thesisTitle))
        if len(thesis) > 0:
            self.success(thesis[0].thesisStatus)
        self.error("Thesis not found")

    @db_session
    def get_thesis_text_by_thesis_id(self, id):
        if len(Thesis[id]) > 0:
            self.success(Thesis[id].text)
        self.error("Thesis not found")

    @db_session
    def get_thesis_by_keyword_id(self, keywordId):
        thesis = Thesis.select(lambda t: t.thesis.keywords.contains(keywordId))
        if len(thesis) > 0:
            fin = []
            for special in thesis:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("Thesis not found")

    @db_session
    def get_thesis_list_by_fos_id(self, fosId):
        thesis = Thesis.select(t for t in Thesis if Thesis.fieldOfStudy == fosId)
        self.success(thesis)

    @db_session
    def get_thesis_list_by_thesis_status_id(self, tStatusId):
        thesis = Thesis.select(t for t in Thesis if Thesis.thesisStatus == tStatusId)
        if len(thesis) > 0:
            fin = []
            for special in thesis:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("Thesis not found")



class ThesisDetailsMethods(BaseMethod):

    @db_session
    def edit_thesis_detail(self, columnName, value, detailsId):
        if len(ThesisDetails[detailsId]) > 0:
            d = {columnName : value}
            self.success(ThesisDetails[detailsId].set(**d))

    @db_session
    def get_thesis_details_by_thesis_id(self, thesisId):
        thesisD = ThesisDetails.select(td for td in ThesisDetails if ThesisDetails.thesis == thesisId)
        if len(thesisD) > 0:
            self.success(thesisD)


    @db_session
    def delete_thesis(self, thesisDetailsId):
        if len(ThesisDetails[thesisDetailsId]) > 0:
            self.success(Thesis[thesisDetailsId].delete())
        self.error("Thesis details not found")



class ThesisStatusMethods(BaseMethod):

    @db_session
    def list_all_of_statuses(self):
        tStatus = ThesisStatus.select(tS for tS in ThesisStatus)
        if len(tStatus) > 0:
            fin = []
            for special in tStatus:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def add_thesis_to_thesis_status(self, thesisStatusId, thesisId):
        thesisStatus = ThesisStatus.select(lambda tS: tS.id == thesisStatusId)
        if len(thesisStatus) > 0:
            thesisStatus[0].theses.add(thesisId)
            self.success()
        self.error("Thesis Status not found")

    @db_session
    def edit_fos(self, columnName, value, thesisStatusId):
        if len(ThesisStatus[thesisStatusId]) > 0:
            d = {columnName : value}
            self.success(ThesisStatus[thesisStatusId].set(**d))

    @db_session
    def get_fos_by_id(self, thesisStatusId):
        mts= ThesisStatus.select(lambda fos: fos.id == thesisStatusId)
        if len(mts) > 0:
            self.success(mts[0].to_dict(with_collections=True, related_objects=True))
        self.error("Thesis Status not found")

    @db_session
    def delete_fos(self, thesisStatusId):
        if len(ThesisStatus[thesisStatusId]) > 0:
            self.success(ThesisStatus[thesisStatusId].delete())
        self.error("Thesis Status not found")


class FieldOfStudyMethods(BaseMethod):

    @db_session
    def list_all_of_fos(self):
        foses = FieldOfStudy.select(fOS for fOS in FieldOfStudy)
        if len(foses) > 0:
            fin = []
            for special in foses:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")


    @db_session
    def add_thesis_to_fos(self, fosId, thesisId):
        foses = FieldOfStudy.select(lambda fOS: fOS.id == fosId)
        if len(foses) > 0:
            foses[0].theses.add(thesisId)
            self.success()
        self.error("Field of Study not found")

    @db_session
    def edit_fos(self, columnName, value, fosId):
        if len(FieldOfStudy[fosId]) > 0:
            d = {columnName : value}
            self.success(FieldOfStudy[fosId].set(**d))

    @db_session
    def get_fos_by_id(self, fosId):
        mfos = FieldOfStudy.select(lambda fos: fos.id == fosId)
        if len(mfos) > 0:
            self.success(mfos[0].to_dict(with_collections=True, related_objects=True))
        self.error("Field of Study not found")

    @db_session
    def delete_fos(self, fosId):
        if len(FieldOfStudy[fosId]) > 0:
            self.success(FieldOfStudy[fosId].delete())
        self.error("Field of Study not found")


class KeywordMethods(BaseMethod):

    @db_session
    def list_all_of_keywords(self):
        mKeys = Keyword.select(kW for kW in Keyword)
        if len(mKeys) > 0:
            fin = []
            for special in mKeys:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def get_keywords_by_thesis_id(self, thesisId):
        mKeys = Keyword.select(lambda k: k.thesis.contains(thesisId))
        if len(mKeys) > 0:
            fin = []
            for special in mKeys:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def add_thesis_to_keyword(self, kId, thesisId):
        mKeys = Keyword.select(lambda kiword: kiword.id == kId)
        if len(mKeys) > 0:
            mKeys[0].theses.add(thesisId)
            self.success()
        self.error("Keyword not found")

    @db_session
    def edit_keyword(self, columnName, value, keyId):
        if len(Keyword[keyId]) > 0:
            d = {columnName : value}
            self.success(Keyword[keyId].set(**d))

    @db_session
    def get_keyword_by_id(self, keyId):
        mkey = Keyword.select(lambda keyw: keyw.id == keyId)
        if len(mkey) > 0:
            self.success(mkey[0].to_dict(with_collections=True, related_objects=True))
        self.error("Keyword not found")

    @db_session
    def delete_keyword(self, keyId):
        if len(Keyword[keyId]) > 0:
            self.success(Keyword[keyId].delete())
        self.error("Keyword not found")


class LevelMethods(BaseMethod):

    @db_session
    def list_all_of_levels(self):
        mlevel = Level.select(lV for lV in Level)
        if len(mlevel) > 0:
            fin = []
            for special in mlevel:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def get_level_by_user_id(self, userId):
        mlevel = Level.select(lambda l: l.users.contains(userId))
        if len(mlevel) > 0:
            self.success(mlevel)
        self.error("Levels not found")

    @db_session
    def add_user_to_level(self, levelId, userId):
        mlevel = Level.select(lambda lvl: lvl.id == levelId)
        if len(mlevel) > 0:
            mlevel[0].users.add(userId)
            self.success()
        self.error("Level not found")

    @db_session
    def edit_level(self, columnName, value, lvlId):
        if len(Level[lvlId]) > 0:
            d = {columnName : value}
            self.success(Level[lvlId].set(**d))

    @db_session
    def get_level_by_id(self, lvlId):
        mlevel = Level.select(lambda lvl: lvl.id == lvlId)
        if len(mlevel) > 0:
            self.success(mlevel[0].to_dict(with_collections=True, related_objects=True))
        self.error("Level not found")

    @db_session
    def delete_level(self, lvlId):
        if len(Level[lvlId]) > 0:
            self.success(Level[lvlId].delete())
        self.error("Level not found")


