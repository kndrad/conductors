from IVU.allocations.providers import IVUTimetableAllocationProvider, IVUAllocationIDProvider, \
    IVUAllocationScheduleProvider
from IVU.abstracts.resources import IVUResource


class IVUTimetableAllocationsResource(IVUResource):
    def fetch(self, date):
        factory = IVUTimetableAllocationProvider(self._server, date)
        allocations = factory.run()
        return allocations


class IVUAllocationScheduleResource(IVUResource):
    def fetch(self, title, date):
        factory = IVUAllocationIDProvider(self._server, title, date)

        try:
            id = factory.run()
        except TypeError:
            return {}
        else:
            factory = IVUAllocationScheduleProvider(self._server, id, date)
            schedule = factory.run()
            return schedule
