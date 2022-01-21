from abc import ABC

from .requests import (
    IVUTimetableAllocationsRequest,
    IVUAllocationIDRequest,
    IVUAllocationActionsRequest,
    IVUTrainCrewRequest
)


class IVUResourceFactory(ABC):
    request_cls = None

    def __init__(self, server, *args, **kwargs):
        self._server = server
        self._request = self.request_cls(*args, **kwargs)

    def run(self):
        if not self.request_cls:
            raise AttributeError('could not find request class attr in IVUFactory subclass;')

        response = self._server.send(request=self._request)
        parser = self._request.response_parser(response)
        result = parser.perform()
        return result


class IVUTimetableAllocationsFactory(IVUResourceFactory):
    request_cls = IVUTimetableAllocationsRequest


class IVUAllocationIDFactory(IVUResourceFactory):
    request_cls = IVUAllocationIDRequest


class IVUAllocationActionsFactory(IVUResourceFactory):
    request_cls = IVUAllocationActionsRequest


class IVUTrainCrewFactory(IVUResourceFactory):
    request_cls = IVUTrainCrewRequest
