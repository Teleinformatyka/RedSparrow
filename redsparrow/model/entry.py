"""Representation of the entry(text) in DB"""
import json
import copy

class Document(object):
    table_name = 'document'

    def __init__(self, id=0, text='', file_path=''):
        self.id = id
        self.text = text
        self.file_path = file_path


    def __str__(self):
        return json.dumps(self.__dict__)

    def insert(self):
        query = "INSERT INTO `%s` " % Document.table_name
        colums = values = ''
        data = copy.deepcopy(self.__dict__)
        del data['id']
        print(list(data.keys()))
        keys ="`" +  "`,`".join(list(data.keys())) + "`"
        values ="`" +  "`,`".join(list(data.values())) + "`"
        query +=  '(%s)  VALUES (%s)' % (keys, values)
        return query





