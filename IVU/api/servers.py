from requests import Session

from . import IVUServerAuthenticationError, IVUServerConnectionNotEstablishedError
from .requests import IVURequest

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36',
    'Referer': 'https://irena1.intercity.pl/mbweb/main/matter/desktop/main-menu'
}

class IVUServer:

    def __init__(self):
        self.session = Session()
        self._connection_established = False

    def login(self, username, password):
        authenticated = False

        with self.session as session:
            self.session.headers.update(HEADERS)
            response = session.get(
                url='https://irena1.intercity.pl/mbweb/main/matter/desktop/',
                headers=HEADERS
            )
            response.raise_for_status()

            payload = {
                'j_username': username.lower().strip(),
                'j_password': password.strip(),
            }
            self.session.headers.update(HEADERS)
            response = self.session.post(
                url='https://irena1.intercity.pl/mbweb/j_security_check',
                data=payload, headers=HEADERS
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
        response = self.session.send(request)
        response.raise_for_status()
        return response
