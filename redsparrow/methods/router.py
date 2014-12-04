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
        self.__methods = {}

    def add_method(self, method):
        self.__add_method(method.name, method)

    def __add_method(self, name, method):
        method.application = self.__application
        logging.info('Adding {}'.format(name))
        self.__methods[name] = method

    def add_methods(self, methods):
        for method in methods:
            self.__add_method(method[0], method[1]())

    # @process
    def find_method(self, message):
        method_name = message.method
        try:
            method = self.__methods[message.method]
            if '-' in message.method:
                method_name = message.method.split('-')[1]
                getattr(method, method_name)(**message.params)
            else:
                method.process(**message.params)
        except KeyError as err:
            logging.error("Method {} not found!".format(message.method))
            message.error = "Method not found"
            self.__application.send_response(message)



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
        return [a for a in inspect.getargspec(method).args if a not in ["self"]]

        exclusions = []

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
            auto_routes.append((class_name.lower(), class_obj))
            for method in methods_keys:
                if not method.startswith('_'):
                    # auto_routes[class_name.lower()].append( { method.lower(): yield_args(module, class_name, method)})
                    auto_routes.append(('-'.join((class_name.lower(), method)), class_obj))

    return auto_routes
