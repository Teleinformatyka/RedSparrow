from pony.orm import *
from datetime import date

from redsparrow.config import Config

db = Database()
db.bind('mysql', user=Config['database']['user'], passwd=Config['database']['password'],
        host=Config['database']['host'], db=Config['database']['database'])


class Thesis(db.Entity):
    _table_ = "Thesis"
    id = PrimaryKey(int, size=16, auto=True, column="ID")
    thesisStatus = Required("ThesisStatus", column="Thesis_Status_ID")
    fieldOfStudy = Required("FieldOfStudy", column="Field_of_Study_ID")
    title = Required(str, 120, column="Title")
    filename = Required(str, 40, column="File_Name")
    filenameHash = Required(str, 40, column="File_Name_Hash")
    dateOfAlligance = Required(date, column="Data_of_Alligance")
    thesisDetails = Optional("ThesisDetails")
    users = Set("User", table="User_Thesis", column="User_ID")


class ThesisDetails(db.Entity):
    _table_ = "Thesis_Details"
    id = PrimaryKey(int, size=16, auto=True, column="ID")
    thesis = Required(Thesis, column="Thesis_ID")
    words = Required(int, size=16, column="Words")
    chars = Required(int, size=24, column="Chars")
    qoutes = Required(int, size=16, column="Quotes")
    sentences = Required(int, size=16, column="Sentences")


class ThesisStatus(db.Entity):
    _table_ = "Thesis_Status"
    id = PrimaryKey(int, size=8, auto=True, column="ID")
    status = Required(str, 9, column="Status")
    theses = Set(Thesis)


class FieldOfStudy(db.Entity):
    _table_ = "Field_of_Study"
    id = PrimaryKey(int, size=8, auto=True, column="ID")
    fos = Required(str, 31, column="FoS")
    theses = Set(Thesis)


class User(db.Entity):
    _table_ = "User"
    id = PrimaryKey(int, size=16, auto=True, column="ID")
    login = Required(str, 30, column="Login")
    password = Required(str, 56, column="Password")
    email = Required(str, 120, column="E_mail")
    name = Required(str, 30, column="Name")
    surname = Required(str, 60, column="Surname")
    theses = Set(Thesis, column="Thesis_ID")
    levels = Set("Level", table="User_Level", column="Level_ID")


class Level(db.Entity):
    _table_ = "Level"
    id = PrimaryKey(int, size=8, auto=True, column="ID")
    level = Required(str, 9, column="Level")
    users = Set(User, column="User_ID")


db.generate_mapping(check_tables=True, create_tables=True)