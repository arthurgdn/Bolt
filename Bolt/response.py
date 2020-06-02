from .http_utils import utf8_bytes
class Response(object):
    """
    Container for data related to an HTTP response that
    can translate itself into a series of bytes.
    """
    reason_phrases = {
        200: 'OK',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        451: 'Unavailable for Legal Reasons',
        500: 'Internal Server Error',
    }

    def __init__(self, code=200, body=b'', **kwargs):
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

    def to_bytes(self):
        return self._build_response()