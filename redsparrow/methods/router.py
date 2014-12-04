import logging
import tornado

import pyclbr
import pkgutil
import importlib
import inspect
from itertools import chain
from functools import reduce

from redsparrow.database.adisp import process, async

from tornado_json.utils import extract_method


class Router(object):

    def __init__(self, application):
        self.__application = application
        self.__methods_class = {}

    def add_method(self, method):
        self.__add_method(method.name, method)

    def __add_method(self, name, method, original_name='process'):
        method.application = self.__application
        logging.info('Adding {}'.format(name))
        self.__methods_class[name] = (method, original_name)

    def add_methods(self, methods):
        for method in methods:
            self.__add_method(method['name'], method['class'](), method['original_name'])

    # @process
    def find_method(self, message):
        try:
            class_obj, original_name = self.__methods_class[message.method]
            class_obj.request = message

        except KeyError as err:
            logging.error("Method {} not found!".format(message.method))
            message.error = { 'code': -32601, 'message': "Method not found"}
            self.__application.send_response(message)
            return

        try:
            getattr(class_obj, original_name)(**message.params)
        except TypeError:
            getattr(class_obj, original_name)(message.params)





# stolen from https://github.com/hfaran/Tornado-JSON/blob/master/tornado_json/routes.py
def get_methods(package):
    """
    This will walk ``package`` and generates method list from any and all
    ``BaseMethod``it finds.     :type  package: package
    :param package: The package containing RequestHandlers to generate
        routes from
    :returns: List of methods for all submodules of ``package``
    :rtype: [(method, BaseMethod), ... ]
    """
    return list(chain(*[get_module_routes(modname) for modname in
                        gen_submodule_names(package)]))


def gen_submodule_names(package):
    """Walk package and yield names of all submodules

    :type  package: package
    :param package: The package to get submodule names of
    :returns: Iterator that yields names of all submodules of ``package``
    :rtype: Iterator that yields ``str``
    """
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=package.__path__,
        prefix=package.__name__ + '.',
            onerror=lambda x: None):
        yield modname


def get_module_routes(module_name, custom_routes=None, exclusions=None):
    """Create and return routes for module_name

    """

    def yield_args(module, cls_name, method_name):
        """Get signature of ``module.cls_name.method_name``

        Confession: This function doesn't actually ``yield`` the arguments,
            just returns a list. Trust me, it's better that way.

        :returns: List of arg names from method_name except ``self``
        :rtype: list
        """
        wrapped_method = reduce(getattr, [module, cls_name, method_name])
        method = extract_method(wrapped_method)
        return [a for a in inspect.signature(method).parameters if a not in ["self"]]

    # Import module so we can get its request handlers
    module = importlib.import_module(module_name)

    # Generate list of RequestHandler names in custom_routes

    # rhs is a dict of {classname: pyclbr.Class} key, value pairs
    auto_routes = []
    rhs = pyclbr.readmodule(module_name)
    for class_name, class_pycblr in rhs.items():
        class_obj = getattr(module, class_name)
        if 'BaseMethod'  in class_pycblr.super:
            methods_keys =  class_pycblr.methods.keys()

            # auto_routes[class_name.lower()] = [ {class_name.lower(): yield_args(module, class_name, '_process')}]
            auto_routes.append({'name': class_name.lower(), 'class': class_obj, 'args': yield_args(module, class_name, 'process'), 'original_name': 'process'})
            for method_name in methods_keys:
                if not method_name.startswith('_') and method_name not in ['process']:
                    # auto_routes[class_name.lower()].append( { method.lower(): yield_args(module, class_name, method)})
                    auto_routes.append({ 'name': '-'.join((class_name.lower(), method_name)), 'class': class_obj, 'args': yield_args(module, class_name, method_name), 'original_name': method_name})

    return auto_routes
