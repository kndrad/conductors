from requests import Session

from facades.irena import AuthenticationError, UnauthenticatedError
from facades.irena.requests import IrenaRequest


class IrenaClient:
    def authenticate(self):
        """Tries to authenticate the user by sending a request to https://irena1.intercity.pl/mbweb/j_security_check
        with session and credentials.
        """
        with self._session as session:
            url = 'https://irena1.intercity.pl/mbweb/main/matter/desktop/'
            session.get(url=url).raise_for_status()
            url = 'https://irena1.intercity.pl/mbweb/j_security_check'

            response = self._session.post(url=url, data=self._credentials)
            response.raise_for_status()

            if response.request.path_url == '/mbweb/login?login-status=failed':
                raise AuthenticationError(self._credentials)

        return True

    def __init__(self, username, password, authenticate=True):
        self._session = Session()
        self._credentials = {
            'j_username': username.lower().strip(),
            'j_password': password.strip(),
        }

        if authenticate:
            self._authenticated = self.authenticate()
        else:
            self._authenticated = False

    def get_response(self, request: IrenaRequest):
        """Starts by checking if the user is authenticated.
        If not, it raises an UnauthenticatedIrenaClientError() exception.
        Next, the code prepares a request and sends it to the server using self._session.send().
        The response from sending this request is then analyzed and returned as a string in response.
        """
        if not self._authenticated:
            raise UnauthenticatedError()

        request = self._session.prepare_request(request)
        response = self._session.send(request)
        response.raise_for_status()
        return response
