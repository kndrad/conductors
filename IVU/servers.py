from requests import Session

from . import IVUServerAuthenticationError, IVUServerConnectionNotEstablishedError
from IVU.requests import IVURequest


class IVUServer:

    def __init__(self):
        self._session = Session()
        self._connection_established = False

    def login(self, username, password):
        authenticated = False

        with self._session as session:
            url = 'https://irena1.intercity.pl/mbweb/main/matter/desktop/'
            session.get(url=url).raise_for_status()
            url = 'https://irena1.intercity.pl/mbweb/j_security_check'

            payload = {
                'j_username': username.lower().strip(),
                'j_password': password.strip(),
            }

            response = self._session.post(url=url, data=payload)
            response.raise_for_status()

            if response.request.path_url == '/mbweb/login?login-status=failed':
                raise IVUServerAuthenticationError()
            else:
                authenticated = True

        self._connection_established = authenticated
        return authenticated

    def ask(self, request: IVURequest):
        if not self._connection_established:
            raise IVUServerConnectionNotEstablishedError()

        request = self._session.prepare_request(request)
        response = self._session.send(request)
        response.raise_for_status()
        return response
