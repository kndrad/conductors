import abc

from .factories import (
    IVUTimetableAllocationsFactory,
    IVUAllocationIDFactory,
    IVUAllocationActionsFactory,
    IVUCrewMembersFactory
)


class IVUResource:

    def __init__(self, server):
        self._server = server

    @abc.abstractmethod
    def fetch(self, *args, **kwargs):
        pass


class IVUTimetableAllocations(IVUResource):
    def fetch(self, date):
        factory = IVUTimetableAllocationsFactory(self._server, date)
        allocations = factory.run()
        return allocations


class IVUAllocationActions(IVUResource):
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


class IVUCrewMembers(IVUResource):
    def fetch(self, trip, date):
        factory = IVUCrewMembersFactory(self._server, trip, date)
        members = factory.run()
        return members
