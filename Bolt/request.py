class Request(object):
    """
    Container for data related to an HTTP request.
    """
    def __init__(self):
        self.method = None
        self.path = None
        self.query_params = {}
        self.path_params = {}
        self.headers = {}
        self.body = None
        self.body_raw = None
        self.finished = False
