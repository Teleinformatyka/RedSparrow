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
    levels = Set("Level", table="User_Level", column="level_id")


class Level(db.Entity):
    _table_ = "Level"
    id = PrimaryKey(int, size=8, auto=True)
    level = Required(str, 9)
    users = Set(User, column="user_id")


