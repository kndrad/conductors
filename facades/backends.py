import requests
from allauth.account.auth_backends import AuthenticationBackend
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from users.models import User
from .interface import IrenaFacade
from .irena import AuthenticationError


def fetch_credentials(request):
    username = getattr(request.user, settings.ACCOUNT_AUTHENTICATION_METHOD, None)

    if not username:
        raise ValueError(f'invalid authentication field value - got {username}')

    password = request.session.get(settings.SESSION_PASSWORD_KEY)

    if not password:
        raise ValueError(f'seems like no password has been saved in request session, value is {password}')

    return username, password


class IrenaFacadeAuthenticationBackend(AuthenticationBackend):

    def authenticate(self, request, **credentials):
        """Authenticates using Irena facade.
        Password is stored in request.session object to be used later in views.
        """
        username = credentials.get(settings.ACCOUNT_AUTHENTICATION_METHOD, None)
        password = credentials.get('password') or request.session.get(settings.SESSION_PASSWORD_KEY)

        facade = IrenaFacade(username, password)
        try:
            facade.make_authentication()
        except AuthenticationError:
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


def facade_authentication(request, facade=IrenaFacade):
    username, password = fetch_credentials(request)

    facade = facade(username, password)

    try:
        facade = facade.make_authentication()
    except AuthenticationError:
        return redirect(settings.LOGIN_URL)
    else:
        return facade

