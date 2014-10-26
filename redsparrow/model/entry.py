"""Representation of the entry(text) in DB"""
import json
import copy

class Document(object):
    table_name = 'document'
    max_id = 0

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
        keys ="`" +  "`,`".join(list(data.keys())) + "`"
        char = ['%s'] * len(data.values())
        values =",".join(char)
        query +=  '(%s)  VALUES (%s)' % (keys, values)
        return (query, tuple(data.values()))





