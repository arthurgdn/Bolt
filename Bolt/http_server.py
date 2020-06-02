import asyncio
from .http_connection import HTTPConnection
class HTTPServer(object):
    """
    Contains objects that are shared by HTTPConnections and schedules async
    connections.
    :param router: An object that must expose the 'get_handler' interface.
    :param http_parser: An object that must expose the 'parse_into' interface,
        which works with a Request object and a bytearray.
    :param loop: An object that implements the 'asyncio.BaseEventLoop'
        interface.
    """

    def __init__(self, router, http_parser, loop):
        self.router = router
        self.http_parser = http_parser
        self.loop = loop

    async def handle_connection(self, reader, writer):
        """
        Creates and schedules a HTTPConnection given a set (reader, writer)
        objects.
        :param reader: An object that implements the 'asyncio.StreamReader'
            interface.
        :param writer: An object that implements the 'asyncio.StreamWriter'
            interface.
        """
        connection = HTTPConnection(self, reader, writer)
        asyncio.ensure_future(connection.handle_request(), loop=self.loop)

