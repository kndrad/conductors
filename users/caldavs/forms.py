import caldav
from django import forms

from .models import CalDAVAccount


class CalDAVAccountForm(forms.ModelForm):
    class Meta:
        model = CalDAVAccount
        fields = '__all__'
        exclude = ('last_updated', )
        widgets = {
            'user': forms.HiddenInput(),
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

    def clean(self):
        cleaned_data = super().clean()

        client = caldav.DAVClient(
            url=cleaned_data['url'],
            username=cleaned_data['username'],
            password=cleaned_data['password']
        )

        try:
            client.principal()
        except (caldav.error.AuthorizationError, Exception):
            return self.add_error(
                None,
                'Błąd autoryzacji ze strony serwera CalDAV. Sprawdź dane logowania.'
            )

        return cleaned_data
