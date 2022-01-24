from requests import Session

from . import IVUServerAuthenticationError, IVUServerConnectionNotEstablishedError
from .requests import IVURequest

HEADERS = {
    'Host': 'irena1.intercity.pl',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US, en;q=0.5',
    'Connection': 'keep-alive',
}


class IVUServer:

    def __init__(self):
        self.session = Session()
        self._connection_established = False

    def login(self, username, password):
        authenticated = False

        with self.session as session:
            self.session.headers.update(HEADERS)
            url = 'https://irena1.intercity.pl/mbweb/main/matter/desktop/main-menu'
            response = session.get(url=url, headers=HEADERS)
            response.raise_for_status()

            payload = {
                'j_username': username.lower().strip(),
                'j_password': password.strip(),
            }
            response = self.session.post(url='https://irena1.intercity.pl/mbweb/j_security_check', data=payload)
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
