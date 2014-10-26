import yaml

from .utils import Singleton
from .utils import ListBase


class Config(ListBase):
    """Class cointains configuration of system"""
    __metaclass__ = Singleton

    def __init__(self):
        self.data_val = {}


    @property
    def data(self):
        """Basic property getter"""
        return self.data_val

    @data.setter
    def data(self, value):
        """Basic property setter"""

        if type(value) is list:
            raise ValueError("Unsuported type!")
        self.data_val = value

    def load(self, path_to_file='./config/config.yml'):
        """Method load yaml from file

        :param yamlstring: string containing yaml.
        """
        stream = open(path_to_file, 'r')
        self.data_val = yaml.load(stream)
        stream.close()


    def get(self, key):
        """ Return specify key value

        :param key: string.
        :returns: value of key.
        """
        return self.data_val[key]
