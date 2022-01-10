from IVU.abstracts.providers import IVUResourceProvider
from .requests import IVUTimetableAllocationsRequest, IVUAllocationIDRequest, IVUAllocationActionsRequest


class IVUTimetableAllocationProvider(IVUResourceProvider):
    request = IVUTimetableAllocationsRequest


class IVUAllocationIDProvider(IVUResourceProvider):
    request = IVUAllocationIDRequest


class IVUAllocationScheduleProvider(IVUResourceProvider):
    request = IVUAllocationActionsRequest
