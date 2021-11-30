from alina.irena.requests import (
    IrenaAllocationTimetableRequest, IrenaAllocationSignatureRequest, IrenaAllocationDetailsRequest, IrenaRequest,
    IrenaTripCrewMembersRequest
)


class IrenaParsedResponseFactory:
    """The __init__ method is used to initialize the factory with a client object,
    which is done in this case by calling self._client = client.

    The produce method is where all of the magic happens.
    It starts by getting a response from the server using get_response on _request (the request).
    Then it uses parse_response on _request's parser function to parse out what was returned
    from the server into parsed.
    Finally, parsed gets returned back as a result of produce .

    Contains methods for parsing and producing responses.
    """
    _request: IrenaRequest

    def __init__(self, client, *args, **kwargs):
        self._client = client

    def produce(self):
        response = self._client.get_response(self._request)
        parsed = self._request.parser(response).parse_response()
        return parsed


class IrenaTimetableAllocationsFactory(IrenaParsedResponseFactory):
    def __init__(self, client, date, *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self._request = IrenaAllocationTimetableRequest(date)


class IrenaAllocationSignatureFactory(IrenaParsedResponseFactory):
    def __init__(self, client, title, date, *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self._request = IrenaAllocationSignatureRequest(title, date)


class IrenaAllocationDetailsFactory(IrenaParsedResponseFactory):
    def __init__(self, client, signature, date, *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self._request = IrenaAllocationDetailsRequest(signature, date)


class IrenaTripCrewMembersFactory(IrenaParsedResponseFactory):
    def __init__(self, client, number, date, *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self._request = IrenaTripCrewMembersRequest(number, date)
