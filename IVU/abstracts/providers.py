from abc import ABC


class IVUResourceProvider(ABC):
    request = None

    def __init__(self, server, *args, **kwargs):
        self._server = server
        self._request = self.request(*args, *kwargs)

    def run(self):
        if not self.request:
            raise AttributeError('could not find request attr in IVUFactory subclass;')

        response = self._server.ask(request=self.request)
        parser = self.request.response_parser(response)
        result = parser.perform()
        return result
