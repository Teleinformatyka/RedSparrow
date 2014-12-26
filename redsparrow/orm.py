from pony.orm import *
from datetime import date

from redsparrow.config import Config

db = Database()


class Thesis(db.Entity):
    _table_ = "Thesis"
    id = PrimaryKey(int, size=16, auto=True)
    thesisStatus = Required("ThesisStatus", column="thesis_status_id")
    fieldOfStudy = Required("FieldOfStudy", column="field_of_study_id")
    title = Required(str, 120)
    filename = Required(str, 40)
    filenameHash = Required(str, 40, column="filename_hash")
    dateOfAlligance = Required(date, column="date_of_alligance")
    text = Required(LongUnicode)
    thesisDetails = Optional("ThesisDetails")
    users = Set("User", table="User_Thesis", column="user_id")
    keywords = Set("Keyword", table="Keyword_Thesis", column="keyword_id")
    similarities1 = Set("Similarity", reverse="thesis1")
    similarities2 = Set("Similarity", reverse="thesis2")


class ThesisDetails(db.Entity):
    _table_ = "Thesis_Details"
    id = PrimaryKey(int, size=16, auto=True)
    thesis = Required(Thesis, column="thesis_id")
    words = Required(int, size=16)
    chars = Required(int, size=24)
    qoutes = Required(int, size=16)
    sentences = Required(int, size=16)


class ThesisStatus(db.Entity):
    _table_ = "Thesis_Status"
    id = PrimaryKey(int, size=8, auto=True)
    status = Required(str, 9)
    theses = Set(Thesis)


class FieldOfStudy(db.Entity):
    _table_ = "Field_of_Study"
    id = PrimaryKey(int, size=8, auto=True)
    fos = Required(str, 31)
    theses = Set(Thesis)


class Keyword(db.Entity):
    _table_ = "Keyword"
    id = PrimaryKey(int, size=16, auto=True)
    keyword = Required(str, 50)
    theses = Set(Thesis, column="thesis_id")


class User(db.Entity):
    _table_ = "User"
    id = PrimaryKey(int, size=16, auto=True)
    login = Required(str, 30, unique=True)
    password = Required(str, 32)
    email = Required(str, 120, unique=True)
    name = Required(str, 30)
    surname = Required(str, 60)
    theses = Set(Thesis, column="thesis_id")
    roles = Set("Role", table="User_role", column="role_id")


class Role(db.Entity):
    _table_ = "Role"
    id = PrimaryKey(int, size=8, auto=True)
    role = Required(str, 9)
    users = Set(User, column="user_id")

class LinesWords(db.Entity):
    _table_ = "Lines_Words"
    id = PrimaryKey(int, size=16, auto=True)
    similarity = Required('Similarity', reverse="linesWords")
    thesis1LineStart = Required(str, 5, column="thesis1_line_start")
    thesis2LineStart = Required(str, 5, column="thesis2_line_start")
    thesis1LineEnd = Required(str, 5, column="thesis1_line_end")
    thesis2LineEnd = Required(str, 5, column="thesis2_line_end")
    thesis1WordStart = Required(str, 5, column="thesis1_word_start")
    thesis2WordStart = Required(str, 5, column="thesis2_word_start")
    thesis1WordEnd = Required(str, 5, column="thesis1_word_end")
    thesis2WordEnd = Required(str, 5, column="thesis2_word_end")


class Similarity(db.Entity):
    _table_ = "Similarity"
    id = PrimaryKey(int, size=16, auto=True)
    thesis1 = Required(Thesis, reverse="similarities1")
    thesis2 = Required(Thesis, reverse="similarities2")
    percentageSimilarity = Required(int, size=8, column="percentage_similarity")
    keywordSimilarity = Required(int, size=8, column="keyword_similarity")
    similarWords = Required(int, column="similar_words")
    linesWords = Set(LinesWords, reverse="similarity")

