from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from common.forms import HiddenInputUserForm
from .services import stations_exist
from .models import RailroadAccount
from .models import VerifiedStation


def already_verified(stations):
    try:
        for name in stations:
            VerifiedStation.objects.get(name__iexact=name)
    except VerifiedStation.DoesNotExist:
        return False
    else:
        return True


class RailroadAccountModelForm(HiddenInputUserForm, forms.ModelForm):
    class Meta:
        model = RailroadAccount
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'

    def clean(self):
        cleaned_data = super().clean()
        stations = [cleaned_data['homeplace'].lower(), cleaned_data['workplace'].lower()]

        if stations[0] == stations[1]:
            return self.add_error(
                NON_FIELD_ERRORS, 'Podane stacje są takie same. '
                                  'Należy wpisać stacje, które się od siebie różnią.',
            )

        verified = already_verified(stations)
        if not verified:
            if stations_exist(stations[0], stations[1]):
                for name in stations:
                    VerifiedStation.objects.get_or_create(name=name)
            else:
                return self.add_error(
                    NON_FIELD_ERRORS, 'Podane stacje kolejowe nie istnieją. Proszę sprawdzić, czy nie wkradła się '
                                      'literówka.',
                )
        return cleaned_data
