import requests
from allauth.account.auth_backends import AuthenticationBackend
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from IVU.api import IVUServerAuthenticationError
from users.models import User
from IVU.api.servers import IVUServer


def get_credentials(request):
    username = getattr(request.user, settings.ACCOUNT_AUTHENTICATION_METHOD, None)

    if not username:
        raise ValueError(f'invalid authentication field value - got {username}')

    password = request.session.get(settings.SESSION_PASSWORD_KEY)

    if not password:
        raise ValueError(f'seems like no password has been saved in request session, value is {password}')

    return username, password


class IVUServerAuthenticationBackend(AuthenticationBackend):

    def authenticate(self, request, **credentials):
        """Authenticates using IVUServer.
        On success, password is stored in request.session object to be used later in views.
        """
        username = credentials.get(settings.ACCOUNT_AUTHENTICATION_METHOD, None)
        password = credentials.get('password') or request.session.get(settings.SESSION_PASSWORD_KEY)

        server = IVUServer()
        try:
            server.login(username, password)
        except IVUServerAuthenticationError:
            raise ValidationError('Nieprawidłowy email lub hasło. Sprawdź dane logowania.')
        except requests.HTTPError:
            raise ValidationError('Wystąpił błąd. Spróbuj ponownie później')
        else:
            request.session[settings.SESSION_PASSWORD_KEY] = password

        data = {
            settings.ACCOUNT_AUTHENTICATION_METHOD: username
        }

        user = User.objects.get_or_create_passwordless(**data)
        return user


def get_server_or_redirect(request):
    username, password = get_credentials(request)
    server = IVUServer()

    try:
        server.login(username, password)
    except IVUServerAuthenticationError:
        return redirect(settings.LOGIN_URL)
    else:
        return server
