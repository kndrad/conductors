from django import forms

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


class WaypointForm(forms.ModelForm):
    class Meta:
        model = Waypoint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'

