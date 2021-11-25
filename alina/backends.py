import requests
from allauth.account.auth_backends import AuthenticationBackend
from django.core.exceptions import ValidationError

from users.models import User
from .interface import Alina
from .tools.utils import STORED_PASSWORD_KEY
from .irena import IrenaCredentialsDeniedError


class AlinaAuthenticationBackend(AuthenticationBackend):

    def authenticate(self, request, **credentials):
        """Authenticates using Alina.
        Password is stored in request.session object, so they can be used later in views.
        """
        email = credentials.get('email', credentials.get('email')) or request.session.get('email')
        password = credentials.get('password') or request.session.get(STORED_PASSWORD_KEY)

        try:
            alina = Alina(email, password, authenticate=False)
            alina.authenticate()
        except IrenaCredentialsDeniedError:
            raise ValidationError('Nieprawidłowy email lub hasło. Sprawdź dane logowania.')
        except requests.HTTPError:
            raise ValidationError('Wystąpił błąd. Spróbuj ponownie później')

        request.session[STORED_PASSWORD_KEY] = password

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_non_password_user(email=email)
            return user
        else:
            return user
