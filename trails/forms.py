from collections import Counter

from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import inlineformset_factory

from common.forms import HiddenInputUserForm
from trails.models import Trail, Waypoint


class TrailForm(HiddenInputUserForm, forms.ModelForm):

    class Meta:
        model = Trail
        fields = '__all__'

        widgets = HiddenInputUserForm.Meta.widgets
        widgets['last_driven'] = forms.DateInput(attrs={'type': 'date'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['start'].lower().strip() == cleaned_data['end'].lower().strip():
            raise ValidationError('Początek i koniec szlaku nie może być taki sam.')

        return cleaned_data


class WaypointForm(forms.ModelForm):

    class Meta:
        model = Waypoint
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Nazwy stacji nie mogą się powtarzać',
            },
        }
        labels = {'name': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-3 text-base'
