from requests import Request

from . import date_regex, DateRegexError, text_regex, TextRegexError
from .parsers.responses import (
    IVUTimetableAllocationsRequestResponseParser,
    IVUAllocationActionsRequestResponseParser,
    IVUAllocationIDRequestResponseParser,
    IVUTrainCrewRequestResponseParser,
)


class IVURequest(Request):
    response_parser = None

    def __init__(self, *args, **kwargs):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Accept-Language': 'pl-PL',
            'Accept-Encoding': 'gzip, deflate',
        }
        super().__init__(headers=headers, method='GET', *args, **kwargs)


class IVURequestWithDateValue(IVURequest):
    fmt = '%Y-%m-%d'

    def __init__(self, date, *args, **kwargs):
        if not date_regex.match(date):
            raise DateRegexError(date)
        super().__init__(*args, **kwargs)


class IVURequestWithTextValue(IVURequest):
    def __init__(self, text, *args, **kwargs):
        if not text_regex.match(text):
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


class IVUTrainCrewRequest(IVURequestWithTextValue, IVURequestWithDateValue):
    response_parser = IVUTrainCrewRequestResponseParser

    def __init__(self, train_number, date, *args, **kwargs):
        url = (f'https://irena1.intercity.pl/mbweb/main/matter/desktop/'
               f'_-crew-on-trip-table?tripNumber={train_number}&beginDate={date}&')
        super().__init__(text=train_number, date=date, url=url, *args, **kwargs)


class IVUTimetableAllocationsRegisterIDRequest(IVURequestWithDateValue):

    def __init__(self, date, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/matter/desktop/_-actual-duties-table?beginDate={date}'
        super().__init__(date=date, url=url, *args, **kwargs)


class IVUAllocationRegisterComponentsRequest(IVURequestWithTextValue):

    def __init__(self, id, *args, **kwargs):
        url = f'https://irena1.intercity.pl/mbweb/main/matter/desktop/actual-duty-details?allocatableId={id}'
        super().__init__(text=id, url=url, *args, **kwargs)
