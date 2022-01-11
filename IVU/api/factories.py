from abc import ABC

from .requests import (
    IVUTimetableAllocationsRequest,
    IVUAllocationIDRequest,
    IVUAllocationActionsRequest,
    IVUCrewMembersRequest
)


class IVUResourceFactory(ABC):
    request = None

    def __init__(self, server, *args, **kwargs):
        self._server = server
        self._request = self.request(*args, *kwargs)

    def run(self):
        if not self.request:
            raise AttributeError('could not find request attr in IVUFactory subclass;')

        response = self._server.send(request=self._request)
        parser = self._request.response_parser(response)
        result = parser.perform()
        return result


class IVUTimetableAllocationsFactory(IVUResourceFactory):
    request = IVUTimetableAllocationsRequest


class IVUAllocationIDFactory(IVUResourceFactory):
    request = IVUAllocationIDRequest


class IVUAllocationActionsFactory(IVUResourceFactory):
    request = IVUAllocationActionsRequest


class IVUCrewMembersFactory(IVUResourceFactory):
    request = IVUCrewMembersRequest
