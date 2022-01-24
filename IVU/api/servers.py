from requests import Session

from . import IVUServerAuthenticationError, IVUServerConnectionNotEstablishedError
from .requests import IVURequest


class IVUServer:

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}

    def __init__(self):
        self.session = Session()
        self._connection_established = False

    def login(self, username, password):
        authenticated = False

        with self.session as session:
            response = session.get(
                url='https://irena1.intercity.pl/mbweb/main/matter/desktop/',
                headers=self.HEADERS
            )
            response.raise_for_status()

            payload = {
                'j_username': username.lower().strip(),
                'j_password': password.strip(),
            }
            self.session.headers.update(self.HEADERS)
            response = self.session.post(
                url='https://irena1.intercity.pl/mbweb/j_security_check',
                data=payload, headers=self.HEADERS
            )
            response.raise_for_status()

            if response.request.path_url == '/mbweb/login?login-status=failed':
                raise IVUServerAuthenticationError()
            else:
                authenticated = True

        self._connection_established = authenticated
        return authenticated

    def send(self, request: IVURequest):
        if not self._connection_established:
            raise IVUServerConnectionNotEstablishedError()

        request = self.session.prepare_request(request)
        self.session.headers.update(self.HEADERS)
        response = self.session.send(request)
        response.raise_for_status()
        return response
