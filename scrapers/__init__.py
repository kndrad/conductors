class IVUServerError(Exception):
    pass


class IVUServerConnectionError(IVUServerError):
    def __init__(self):
        super().__init__(
            'tried make request to a server while connection is not established;'
            'please authenticate first;'
        )


class IVUServerAuthenticationError(IVUServerError):
    pass
