import logging
from .http_utils import utf8_bytes
from .exceptions import UnknownStatus
class Response(object):
    """
    Container for data related to an HTTP response that
    can translate itself into a series of bytes.
    """
    reason_phrases = {
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        306: 'Switch Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407:' Proxy Authentication Required',
        408: 'Request Timeout',
        429: 'Too Many Requests',
        451: 'Unavailable for Legal Reasons',
        500: 'Internal Server Error',
        502: 'Bad Gataway',
        503: 'Service Unavailable'
    }

    def __init__(self,connection, code=200, body=b'', **kwargs):
        self.connection = connection
        self.code = code
        self.body = body
        self.headers = kwargs.get('headers', {})
        self.headers['content-type'] = kwargs.get('content_type', 'text/html')

    def _build_response(self, encoding_fn=utf8_bytes):
        """
        Translates self into a series of bytes.
        :param encoding_fn: The function responsible for encoding strings
            into bytes using the *correct charset*.
        :return: A bytes object representing the HTTP response.
        """
        if(self.body==b''):
            logging.error('Response error : response was never sent')
            
        
        response_line = 'HTTP/1.1 {0} {1}'.format(
            self.code, self.reason_phrases[self.code])
        self.headers = {**self.headers, **{'Content-Length': len(self.body)}}
        headers = '\r\n'.join(
            [': '.join([k, str(v)]) for k, v in self.headers.items()])
        headers += '\r\n'
        return b'\r\n'.join(map(
            encoding_fn, [response_line, headers, self.body]))

    def set_header(self, header, value=b''):
        """
        Helper method to set a HTTP header.
        :param header: A string with the headername.
        :param value: A bytes object - value of the header.
        """
        self.headers[header] = value

    def set_status(self, status):
        """
        Helper method to set a HTTP status code.
        :param status: An int - value of the status
        """
        if status not in self.reason_phrases.keys():
            logging.error('Response error: unknow HTTP status code ' + str(status))
            raise UnknownStatus
        else: 
            self.code = status

    def to_bytes(self):
        return self._build_response()
    async def send(self,body=''):
        self.body = body
        await self.connection.write(self)
        