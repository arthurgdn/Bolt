class BoltException(Exception):
    pass


class NotFoundException(BoltException):
    code = 404


class BadRequestException(BoltException):
    code = 400


class DuplicateRoute(BoltException):
    pass

class UnknownStatus(BoltException):
    pass

class TimeoutException(BoltException):
    code = 500