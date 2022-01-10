import abc


class IVUResource:

    def __init__(self, server):
        self._server = server

    @abc.abstractmethod
    def fetch(self, *args, **kwargs):
        pass
