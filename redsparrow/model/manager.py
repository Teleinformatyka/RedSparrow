
class Manager:

    def __init__(self, dbconn):
        self.dbconn = dbconn

    def find(self, *args, **kwargs):
        pass

    def save(self, model, callback):
        self.dbconn.runOperation(model.insert(), callback)

