class IrenaError(Exception):
    """Error for Irena"""


class UnauthenticatedIrenaClientError(IrenaError):
    """Raised when IrenaClient wants to make request to irena1.intercity.pl while being unauthenticated.
    """

    def __init__(self):
        super().__init__('tried to perform an action while being unauthenticated;')


class IrenaCredentialsDeniedError(IrenaError):
    """Raised on authentication.
    """

    def __init__(self, credentials):
        super().__init__(f'{credentials};')