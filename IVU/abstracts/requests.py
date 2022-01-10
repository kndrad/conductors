from requests import Request


class IVURequest(Request):
    response_parser = None

    def __init__(self, *args, **kwargs):
        headers = {
            'Accept-Language': 'pl-PL',
            'Accept-Encoding': 'gzip, deflate',
        }
        super().__init__(headers=headers, method='GET', *args, **kwargs)
