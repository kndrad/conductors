from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import RailroadStation
from .models import RailroadAccount
from .engines import RailroadSearchEngine, WaypointStationSubmitError


class RailroadAccountForm(forms.ModelForm):

    class Meta:
        model = RailroadAccount
        fields = '__all__'
        exclude = ('last_updated',)
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'

    def clean(self):
        cleaned_data = super().clean()
        departure_station, arrival_station = cleaned_data['homeplace'].lower(), cleaned_data['workplace'].lower()

        if departure_station == arrival_station:
            return self.add_error(
                NON_FIELD_ERRORS, 'Podane stacje są takie same. '
                                  'Należy wpisać stacje, które się od siebie różnią.',
            )
        try:
            for station in [departure_station, arrival_station]:
                RailroadStation.objects.get(name__iexact=station)
        except RailroadStation.DoesNotExist:
            engine = RailroadSearchEngine()
            stations_exist = engine.check_stations_existence(departure_station, arrival_station)

            if not stations_exist:
                return self.add_error(
                    NON_FIELD_ERRORS, 'Podane stacje kolejowe nie istnieją. Proszę sprawdzić, czy nie wkradła się '
                                      'literówka.',
                )
            else:
                for station in [departure_station, arrival_station]:
                    RailroadStation.objects.get_or_create(name=station)

        return cleaned_data
