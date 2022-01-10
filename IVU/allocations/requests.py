from ..requests import IVUDatedRequest, IVUTextRequest
from .parsers.responses import (
    IVUTimetableAllocationsRequestResponseParser,
    IVUAllocationActionsRequestResponseParser,
    IVUAllocationIDRequestResponseParser,
)


class IVUTimetableAllocationsRequest(IVUDatedRequest):
    response_parser = IVUTimetableAllocationsRequestResponseParser

    def __init__(self, date, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/matter/desktop/_-duty-table?beginDate={date}'
        super().__init__(date=date, url=url, *args, **kwargs)


class IVUAllocationIDRequest(IVUTextRequest, IVUDatedRequest):
    response_parser = IVUAllocationIDRequestResponseParser

    def __init__(self, title, date, *args, **kwargs):
        url = (f'https://irena1.intercity.pl/mbweb/main/ivu/desktop/'
               f'_-any-duty-table?division=&depot=&abbreviation={title}&date={date}&')
        super().__init__(text=title, date=date, url=url, *args, **kwargs)


class IVUAllocationActionsRequest(IVUTextRequest, IVUDatedRequest):
    response_parser = IVUAllocationActionsRequestResponseParser

    def __init__(self, id, date, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/ivu/desktop/any-duty-details?id={id}&beginDate={date}&'
        super().__init__(text=id, date=date, url=url, *args, **kwargs)