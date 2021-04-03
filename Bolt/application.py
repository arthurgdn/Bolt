import asyncio
import logging
import re

from .exceptions import (
    BoltException,
    NotFoundException,
    DuplicateRoute,
)
from . import http_parser
from .utils import generate_router
from .http_server import HTTPServer

logger = logging.getLogger(__name__)
basic_logger_config = {
    'format': '%(asctime)s [%(levelname)s] %(message)s',
    'level': logging.INFO,
    'filename': None
}
logging.basicConfig(**basic_logger_config)

class App(object):
    """
    Contains the configuration needed to handle HTTP requests.
    """
    def __init__(self,
                 routers,
                 host='127.0.0.1',
                 port=8080,
                 log_level=logging.INFO,
                 http_parser=http_parser):
        """
        :param router: a collection of routes that implements the
            'get_handler' interface.
        :param host: a string that represents and ipv4 address associated
            with the interface that will listen for incoming connections.
        :param port: an int that represents the port on which to listen to.
        :param log_level: an integer representing the logging level, using
            default Python stdlib values.
        :param http_parser: an object that implements 'parse_into' interface.
            Responsible for parsing bytes into Requests objects.
        """
        # create ip address class
        self.router = generate_router(routers)
        self.http_parser = http_parser
        self.host = host
        self.port = port
        self._server = None
        self._connection_handler = None
        self._loop = None

        logger.setLevel(log_level)

    def start_server(self):
        """
        Starts listening asynchronously for TCP connections on a socket and
        passes each connection to the HTTPServer.handle_connection method.
        """
        if not self._server:
            self.loop = asyncio.get_event_loop()
            self._server = HTTPServer(self.router, self.http_parser, self.loop)
            self._connection_handler = asyncio.start_server(
                self._server.handle_connection,
                host=self.host,
                port=self.port,
                reuse_address=True,
                reuse_port=True,
                loop=self.loop)
            print('Starting Bolt v.0.0.1 server')
            logger.info('Starting server on {0}:{1}'.format(
                self.host, self.port))
            self.loop.run_until_complete(self._connection_handler)

            try:
                self.loop.run_forever()
            except KeyboardInterrupt:
                logger.info('Got signal, killing server')
            except BoltException as e:
                logger.error('Critical framework failure:')
                logger.error(e.__traceback__)
            finally:
                self.loop.close()
        else:
            logger.info('Server already started - {0}'.format(self))

    def __repr__(self):
        cls = self.__class__
        if self._connection_handler:
            return '{0} - Listening on: {1}:{2}'.format(
                cls, self.host, self.port)
        else:
            return '{0} - Not started'.format(cls)

