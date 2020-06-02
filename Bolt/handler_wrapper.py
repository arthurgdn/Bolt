class HandlerWrapper(object):
    """
    Helper class that calls a user defined handler with a Request as the first
    argument and route defined parameters as kwargs.
    """
    def __init__(self, handler, path_params):
        self.handler = handler
        self.path_params = path_params
        self.request = None

    async def handle(self, request):
        return await self.handler(request, **self.path_params)


