import re
import logging
from .exceptions import (
    BoltException,
    NotFoundException,
    DuplicateRoute,
)
from .handler_wrapper import HandlerWrapper
from . import http_parser
logger = logging.getLogger(__name__)
class Router(object):
    """
    Container used to add and match a group of routes.
    """
    def __init__(self):
        self.routes = {}

    def add_routes(self, routes):
        for route, fn in routes.items():
            self.add_route(route, fn)
    

    def add_route(self, path, handler):
        """
        Creates a path:function pair for later retrieval by path. The
        path is turned into a regular expression.
        :param path: A string that matches a URL path.
        :param handler: An async function that accepts a request
            and returns a string or Response object.
        """
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route not in self.routes:
            self.routes[compiled_route] = handler
        else:
            raise DuplicateRoute

    def get_handler(self, path,method):
        """
        Retrieves the correct async function to process a request.
        :param path: path part of an HTTP request.
        :return: an function that accepts a request and returns a string or
            Response object.
        """
        logger.debug('Getting handler for: {0}'.format(path))
        for route in self.routes.keys():
            path_params = self.__class__.match_path(route, path)
            if path_params is not None and self.routes[method] is not None:
                handler = self.routes[route][method]
                logger.debug('Got handler for: {0}'.format(path))
                wrapped_handler = HandlerWrapper(handler, path_params)
                return wrapped_handler

        raise NotFoundException()
    """
    The following methods are implementing the routes by passing directly the
    handler associated to the specific request methods
    """
    def get(self,path,handler):
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route in self.routes:
            if "get" not in self.routes[compiled_route]:
                self.routes[compiled_route]["get"] = handler
            else :
                raise DuplicateRoute
        else:
            self.routes[compiled_route] = {"get":handler}
    def post(self,path,handler):
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route in self.routes:
            
            if "post" not in self.routes[compiled_route]:
                self.routes[compiled_route]["post"] = handler
            else :
                raise DuplicateRoute
        else:
            self.routes[compiled_route] = {"post":handler}
    def put(self,path,handler):
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route in self.routes:
            if "put" not in self.routes[compiled_route]:
                self.routes[compiled_route]["put"] = handler
            else :
                raise DuplicateRoute
        else:
            self.routes[compiled_route] = {"put":handler}
    def delete(self,path,handler):
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route in self.routes:
            if "delete" not in self.routes[compiled_route]:
                self.routes[compiled_route]["delete"] = handler
            else :
                raise DuplicateRoute
        else:
            self.routes[compiled_route] = {"delete":handler}
    def patch(self,path,handler):
        compiled_route = self.__class__.build_route_regexp(path)
        if compiled_route in self.routes:
            if "patch" not in self.routes[compiled_route]:
                self.routes[compiled_route]["patch"] = handler
            else :
                raise DuplicateRoute
        else:
            self.routes[compiled_route] = {"patch":handler}

    @classmethod
    def build_route_regexp(cls, regexp_str):
        """
        Turns a string into a compiled regular expression. Parses '{}' into
        named groups ie. '/path/{variable}' is turned into
        '/path/(?P<variable>[a-zA-Z0-9_-]+)'.
        :param regexp_str: a string representing a URL path.
        :return: a compiled regular expression.
        """
        def named_groups(matchobj):
            return '(?P<{0}>[a-zA-Z0-9_-]+)'.format(matchobj.group(1))

        re_str = re.sub(r'{([a-zA-Z0-9_-]+)}', named_groups, regexp_str)
        re_str = ''.join(('^', re_str, '$',))
        return re.compile(re_str)

    @classmethod
    def match_path(cls, route, path):
        """
        Utility function that returns URL parameters if a path matches a route
        or None if it doesn't.
        :param route: a compiled regexp that represents a route.
        :param path: a URL path to be matched against the route.
        :return: Either a dict of URL param:value pairs if path matches the
            route else None.
        """
        match = route.match(path)
        try:
            return match.groupdict()
        except AttributeError:
            return None