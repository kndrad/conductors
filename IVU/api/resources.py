import abc

from .factories import (
    IVUTimetableAllocationsFactory,
    IVUAllocationIDFactory,
    IVUAllocationActionsFactory,
    IVUCrewFactory
)


class IVUResource:

    def __init__(self, server):
        self._server = server

    @abc.abstractmethod
    def fetch(self, *args, **kwargs):
        pass


class IVUTimetableAllocationsResource(IVUResource):
    def fetch(self, date):
        factory = IVUTimetableAllocationsFactory(self._server, date)
        allocations = factory.run()
        return allocations


class IVUAllocationActionsResource(IVUResource):
    def fetch(self, title, date):
        factory = IVUAllocationIDFactory(self._server, title, date)

        try:
            id = factory.run()
        except TypeError:
            return {}
        else:
            factory = IVUAllocationActionsFactory(self._server, id, date)
            actions = factory.run()
            return actions


class IVUCrewResource(IVUResource):
    def fetch(self, trip, date):
        factory = IVUCrewFactory(self._server, trip, date)
        crew = factory.run()
        return crew
