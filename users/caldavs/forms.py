import caldav
from django import forms

from .models import CalDAVAccount


class CalDAVAccountModelForm(forms.ModelForm):
    class Meta:
        model = CalDAVAccount
        fields = '__all__'
        exclude = ('last_updated',)
        widgets = {
            'user': forms.HiddenInput(),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'

    def clean(self):
        cleaned_data = super().clean()

        client = caldav.DAVClient(
            url=cleaned_data['url'],
            username=cleaned_data['username'],
            password=cleaned_data['password']
        )

        try:
            client.principal()
        except caldav.error.AuthorizationError:
            return self.add_error(
                None,
                'Błąd autoryzacji ze strony serwera CalDAV. Sprawdź dane logowania.'
            )
        except caldav.error.DAVError:
            return self.add_error(
                None,
                'Wystąpij błąd podczas próby połączenia z serwerem CalDAV.\n'
                'Upewnij się, czy kalendarz obsługuje aplikacje trzecie.'
            )

        return cleaned_data
