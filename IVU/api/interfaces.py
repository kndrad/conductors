import abc

from .factories import (
    IVUTimetableAllocationsFactory,
    IVUAllocationIDFactory,
    IVUAllocationActionsFactory,
    IVUTrainCrewMembersFactory
)


class IVUResource:
    factory = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def request(self, server):
        resources = self.factory(server, **self.kwargs).run()
        return resources


class IVUTimetableAllocations(IVUResource):
    factory = IVUTimetableAllocationsFactory


class IVUAllocationActions(IVUResource):
    def request(self, server):
        factory = IVUAllocationIDFactory(server, **self.kwargs)

        try:
            id = factory.run()
        except TypeError:
            return {}
        else:
            kwargs = {
                'id' : id,
                'date' : self.kwargs.pop('date')
            }

            factory = IVUAllocationActionsFactory(server, **kwargs)
            actions = factory.run()
            return actions


class IVUTrainCrewMembers(IVUResource):
    factory = IVUTrainCrewMembersFactory
