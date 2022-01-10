from ..requests import IVUTextRequest, IVUDatedRequest
from .parsers.responses import IVUTrainCrewRequestResponseParser


class IVUTrainCrewRequest(IVUTextRequest, IVUDatedRequest):
    response_parser = IVUTrainCrewRequestResponseParser

    def __init__(self, train_number, date, *args, **kwargs):
        url = (f'https://irena1.intercity.pl/mbweb/main/matter/desktop/'
               f'_-crew-on-trip-table?tripNumber={train_number}&beginDate={date}&')
        super().__init__(text=train_number, date=date, url=url, *args, **kwargs)
