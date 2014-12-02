import logging
import tornado

import pyclbr
import pkgutil
import importlib
import inspect
from itertools import chain
from functools import reduce

from redsparrow.database.adisp import process, async

from tornado_json.utils import extract_method, is_method, is_handler_subclass

METHODS = [ '_process']

class Router(object):

    def __init__(self, application):
        self.__application = application
        self.__methods = {}

    def add_method(self, method):
        method.application = self.__application
        logging.info('Adding {}'.format(method.name))
        self.__methods[method.name] = method

    # @process
    def find_method(self, message):
        try:
            method = self.__methods[message.method]
            method.request = message
            method.process(**message.params)
        except KeyError as err:
            logging.error("Method {} not found!".format(message.method))
            message.error = "Method not found"
            self.__application.send_response(message)



# stolen frome https://github.com/hfaran/Tornado-JSON/blob/master/tornado_json/routes.py
def get_routes(package):
    """
    This will walk ``package`` and generates routes from any and all
    ``APIHandler`` and ``ViewHandler`` subclasses it finds. If you need to
    customize or remove any routes, you can do so to the list of
    returned routes that this generates.

    :type  package: package
    :param package: The package containing RequestHandlers to generate
        routes from
    :returns: List of routes for all submodules of ``package``
    :rtype: [(url, RequestHandler), ... ]
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

    Routes are (url, RequestHandler) tuples

    :returns: list of routes for ``module_name`` with respect to ``exclusions``
        and ``custom_routes``. Returned routes are with URLs formatted such
        that they are forward-slash-separated by module/class level
        and end with the lowercase name of the RequestHandler (it will also
        remove 'handler' from the end of the name of the handler).
        For example, a requesthandler with the name
        ``helloworld.api.HelloWorldHandler`` would be assigned the url
        ``/api/helloworld``.
        Additionally, if a method has extra arguments aside from ``self`` in
        its signature, routes with URL patterns will be generated to
        match ``r"(?P<{}>[a-zA-Z0-9_]+)".format(argname)`` for each
        argument. The aforementioned regex will match ONLY values
        with alphanumeric+underscore characters.
    :rtype: [(url, RequestHandler), ... ]
    :type  module_name: str
    :param module_name: Name of the module to get routes for
    :type  custom_routes: [(str, RequestHandler), ... ]
    :param custom_routes: List of routes that have custom URLs and therefore
        should be automagically generated
    :type  exclusions: [str, str, ...]
    :param exclusions: List of RequestHandler names that routes should not be
        generated for
    """
    print(module_name)
    def has_method(module, cls_name, method_name):
        return all([
            method_name in vars(getattr(module, cls_name)),
            is_method(reduce(getattr, [module, cls_name, method_name]))
        ])

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

    def generate_auto_route(module, module_name, cls_name, method_name, url_name):
        """Generate URL for auto_route

        :rtype: str
        :returns: Constructed URL based on given arguments
        """
        def get_handler_name():
            """Get handler identifier for URL

            For the special case where ``url_name`` is
            ``__self__``, the handler is named a lowercase
            value of its own name with 'handler' removed
            from the ending if give; otherwise, we
            simply use the provided ``url_name``
            """
            if url_name == "__self__":
                if cls_name.lower().endswith('handler'):
                    return cls_name.lower().replace('handler', '', 1)
                return cls_name.lower()
            else:
                return url_name

        def get_arg_route():
            """Get remainder of URL determined by method argspec

            :returns: Remainder of URL which matches `\w+` regex
                with groups named by the method's argument spec.
                If there are no arguments given, returns ``""``.
            :rtype: str
            """
            if yield_args(module, cls_name, method_name):
                return "/{}/?$".format("/".join(
                    ["(?P<{}>[a-zA-Z0-9_]+)".format(argname) for argname
                     in yield_args(module, cls_name, method_name)]
                ))
            return r"/?"

        return "/{}/{}{}".format(
            "/".join(module_name.split(".")[1:]),
            get_handler_name(),
            get_arg_route()
        )

    if not custom_routes:
        custom_routes = []
    if not exclusions:
        exclusions = []

    # Import module so we can get its request handlers
    module = importlib.import_module(module_name)

    # Generate list of RequestHandler names in custom_routes
    custom_routes_s = [c.__name__ for r, c in custom_routes]

    # rhs is a dict of {classname: pyclbr.Class} key, value pairs
    auto_routes = {}
    rhs = pyclbr.readmodule(module_name)
    for class_name, class_obj in rhs.items():
        if 'BaseMethod'  in class_obj.super:
            methods_keys =  class_obj.methods.keys()
            auto_routes[class_name.lower()] = [ {class_name.lower(): yield_args(module, class_name, '_process')}]
            for method in methods_keys:
                if '_' not in method:
                    auto_routes[class_name.lower()].append( { method.lower(): yield_args(module, class_name, method)})





    # You better believe this is a list comprehension
    routes = auto_routes
    print(routes)
    return routes
