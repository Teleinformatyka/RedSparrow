
class Singleton(type):
    """ Class for making Singleton object """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ListBase(object):
    """ Class for creating list/dict like object.
    Magic method are implemented.
    """

    @property
    def data(self):
        """Basic property getter"""
        raise NotImplementedError()

    @data.setter
    def data(self, value):
        """Basic property setter"""
        raise NotImplementedError()

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)
