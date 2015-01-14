import os
import tornado
import hashlib
from pony.orm import db_session

from redsparrow.orm import User, Thesis, ThesisDetails, Keyword, Role, ThesisStatus, FieldOfStudy
from .base import BaseMethod
from redsparrow.extractor.gettext import get_text
from redsparrow.keywords import get_keywords
from redsparrow.plagiarism.periodic_detector import ThesesQueue

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

    def __init__(self):
        super(UserMethods, self).__init__('user_methods')

    @db_session
    def edit_user(self, columnName, value, userId):
        if User[userId] is not None:
            d = {columnName : value}
            return self.success(User[userId].set(**d))
        else:
            return self.error('Not found')


    @db_session
    def get_numer_of_users(self):
        users = User.select(u for u in User)[:]
        self.success(len(users))

    @db_session
    def get_user_by_id(self, userId):
        user = User.select(lambda u: u.id == userId)[:]
        if len(user) > 0:
            self.success(user[0].to_dict(with_collections=True, related_objects=True))
        self.error("User not found")

    @db_session
    def delete_user(self, userId):
        if User[userId] is not None:
            print(User[userId])
            User[userId].delete()
            self.success('User with id {} deleted'.format(userId))
        self.error("User not found")

    @db_session
    def add_user_role_by_user_id(self,userId, roleId):
        user = User.select(lambda u: u.id == userId)[:]
        if len(user) > 0:
            user[0].roles.add(roleId)
            self.success()
        self.error("User not found")

    @db_session
    def set_user_password_by_user_id(self, userId, password):
        user = User.select(lambda u: u.id == userId)[:]
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

    def __init__(self):
        super(ThesisMethods, self).__init__('thesis_methods')

    # @tornado.gen.coroutine
    @db_session
    def add_thesis(self, thesis_name, user_id, supervisor_id, fos_id, filepath):
        """
            Add Thesis method
            :param thesis_name: thesis title
            :param user_id: author's id
            :param supervisor_id: thesis supervisor's id
            :param fos_id: field of study's id
            :param keywords: array of keywords
            :param filepath: path to thesis's file
        """
        hasher = hashlib.md5()
        with open(filepath, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        converted_text = get_text(filepath)
        thesis_status = ThesisStatus.select(lambda ts: ts.status == "Waiting")[:]
        if len(thesis_status) == 0:
            return self.error("Unable to find thesis_status")
        thesis = Thesis(title=thesis_name,
                        thesisStatus=thesis_status[0].id,
                        fieldOfStudy=fos_id,
                        filenameHash=hasher.hexdigest(),
                        text=converted_text
                        )
        thesis.users.add(User[user_id])
        thesis.users.add(User[supervisor_id])
        keywords = get_keywords(converted_text)
        for key in keywords:
            keyword = Keyword(keyword=key)
            thesis.keywords.add(keyword)

        # count characters
        c_chars = len(converted_text)
        # count sentences assuming that each sentence ends with . or ! or ?
        c_sentences = converted_text.count('.') + converted_text.count('?') + converted_text.count('!')
        # split at any whitespace
        tempwords = converted_text.split(None)
        c_words = len(tempwords)
        # count quotes
        c_quotes = int(converted_text.count('\"')/2)

        thesis_details = ThesisDetails(thesis=thesis.id,
                                       words=c_words,
                                       chars=c_chars,
                                       quotes=c_quotes,
                                       sentences=c_sentences)
        thesis.thesisDetails = thesis_details
        self.success("ok")

    @db_session
    def get_numer_of_thesis(self):
        thesis = Thesis.select(t for t in Thesis)[:]
        self.success(len(thesis))

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
            Thesis[thesisId].delete()
            self.success("Thesis with {} deleted".format(thesisId))
        self.error("Thesis not found")

    @db_session
    def add_thesis_to_user_by_user_id(self, userId, thesisId):
        self.users.add(userId)
        user = User.select(lambda u: u.id == userId)
        if len(user) > 0:
            self.success(user[0].theses.add(thesisId))


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
    @db_session
    def run_analysis(self, thesis_id):
        """
            run_analysis method get Thesis by thesis_id and process on it PlagiarismDetector

            :param thesis_id: id of thesis to analysis

        """
        thesis = None
        thesis = Thesis.select(lambda t: t.id == thesis_id)[:]

        if len(thesis) == 0:
            return self.error(message="Thesis not found")
        # TODO: change status of thesis
        # thesis[0]
        self.add_to_queue(thesis[0].id)
        self.success("Added to queue")

class ThesisDetailsMethods(BaseMethod):

    def __init__(self):
        super(ThesisDetailsMethods, self).__init__('thesis_details_methods')

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
    def __init__(self):
        super(ThesisStatusMethods, self).__init__('thesis_status_methods')

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
    def edit_thesis_status(self, columnName, value, thesisStatusId):
        if len(ThesisStatus[thesisStatusId]) > 0:
            d = {columnName : value}
            self.success(ThesisStatus[thesisStatusId].set(**d))

    @db_session
    def get_thesis_status_by_id(self, thesisStatusId):
        mts= ThesisStatus.select(lambda fos: fos.id == thesisStatusId)
        if len(mts) > 0:
            self.success(mts[0].to_dict(with_collections=True, related_objects=True))
        self.error("Thesis Status not found")

    @db_session
    def delete_thesis_status(self, thesisStatusId):
        if len(ThesisStatus[thesisStatusId]) > 0:
            self.success(ThesisStatus[thesisStatusId].delete())
        self.error("Thesis Status not found")


class FieldOfStudyMethods(BaseMethod):
    def __init__(self):
        super(FieldOfStudyMethods, self).__init__('field_of_study_methods')

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
    def __init__(self):
        super(KeywordMethods, self).__init__('key_methods')

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


class RoleMethods(BaseMethod):
    def __init__(self):
        super(RoleMethods, self).__init__('role_methods')

    @db_session
    def list_all_of_roles(self):
        mrole = Role.select(rV for rV in Role)
        if len(mrole) > 0:
            fin = []
            for special in mrole:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")

    @db_session
    def get_role_by_user_id(self, userId):
        mrole = Role.select(lambda l: l.users.contains(userId))
        if len(mrole) > 0:
            self.success(mrole)
        self.error("Roles not found")

    @db_session
    def add_user_to_role(self, roleId, userId):
        mrole = Role.select(lambda rl: rl.id == roleId)
        if len(mrole) > 0:
            mrole[0].users.add(userId)
            self.success()
        self.error("Role not found")

    @db_session
    def edit_role(self, columnName, value, rlId):
        if len(Role[rlId]) > 0:
            d = {columnName : value}
            self.success(Role[rlId].set(**d))

    @db_session
    def get_role_by_id(self, rlId):
        mrole = Role.select(lambda rl: rl.id == rlId)
        if len(mrole) > 0:
            self.success(mrole[0].to_dict(with_collections=True, related_objects=True))
        self.error("Role not found")

    @db_session
    def delete_role(self, rlId):
        if len(Role[rlId]) > 0:
            self.success(Role[rlId].delete())
        self.error("Role not found")

class SimilarityMethods(BaseMethod):
    def __init__(self):
        super(SimilarityMethods, self).__init__('similarity_methods')

    @db_session
    def get_numer_of_similarities(self):
        similarities = Similarity.select(s for s in Similarity)[:]
        self.success(len(similarities))

    @db_session
    def list_all_of_similarities(self):
        similarities = Similarity.select(s for s in Similarity)
        if len(similarities) > 0:
            fin = []
            for special in similarities:
                fin.add(special.to_dict(with_collections=True, related_objects=True))
            self.success(fin)
        self.error("List is empty")


