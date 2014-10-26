
import tornado
import logging
from redsparrow.database.adisp import process, async

class Manager:

    def __init__(self, dbconn):
        self.dbconn = dbconn

    def find(self, *args, **kwargs):
        passed

    @process
    def save(self, model, callback):

        result = yield self.dbconn.runOperation(stmt=model.insert())
        callback(result)
        return result

