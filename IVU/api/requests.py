from requests import Request

from . import date_re, DateRegexError, text_re, TextRegexError
from .parsers.responses import (
    IVUTimetableAllocationsRequestResponseParser,
    IVUAllocationActionsRequestResponseParser,
    IVUAllocationIDRequestResponseParser,
    IVUCrewMembersRequestResponseParser,
)


class IVURequest(Request):
    response_parser = None

    def __init__(self, *args, **kwargs):
        headers = {
            'Accept-Language': 'pl-PL',
            'Accept-Encoding': 'gzip, deflate',
        }
        super().__init__(headers=headers, method='GET', *args, **kwargs)


class IVURequestWithDateValue(IVURequest):
    fmt = '%Y-%m-%d'

    def __init__(self, date, *args, **kwargs):
        if not date_re.match(date):
            raise DateRegexError(date)
        super().__init__(*args, **kwargs)


class IVURequestWithTextValue(IVURequest):
    def __init__(self, text, *args, **kwargs):
        if not text_re.match(text):
            raise TextRegexError(text)
        super().__init__(*args, **kwargs)


class IVUTimetableAllocationsRequest(IVURequestWithDateValue):
    response_parser = IVUTimetableAllocationsRequestResponseParser

    def __init__(self, date, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/matter/desktop/_-duty-table?beginDate={date}'
        super().__init__(date=date, url=url, *args, **kwargs)


class IVUAllocationIDRequest(IVURequestWithTextValue, IVURequestWithDateValue):
    response_parser = IVUAllocationIDRequestResponseParser

    def __init__(self, title, date, *args, **kwargs):
        url = (f'https://irena1.intercity.pl/mbweb/main/ivu/desktop/'
               f'_-any-duty-table?division=&depot=&abbreviation={title}&date={date}&')
        super().__init__(text=title, date=date, url=url, *args, **kwargs)


class IVUAllocationActionsRequest(IVURequestWithTextValue, IVURequestWithDateValue):
    response_parser = IVUAllocationActionsRequestResponseParser

    def __init__(self, id, date, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/ivu/desktop/any-duty-details?id={id}&beginDate={date}&'
        super().__init__(text=id, date=date, url=url, *args, **kwargs)


class IVUCrewMembersRequest(IVURequestWithTextValue, IVURequestWithDateValue):
    response_parser = IVUCrewMembersRequestResponseParser

    def __init__(self, trip, date, *args, **kwargs):
        url = (f'https://irena1.intercity.pl/mbweb/main/matter/desktop/'
               f'_-crew-on-trip-table?tripNumber={trip}&beginDate={date}&')
        super().__init__(text=trip, date=date, url=url, *args, **kwargs)
