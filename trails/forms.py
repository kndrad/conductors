from django import forms

from trails.models import Trail, Waypoint


class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = '__all__'
        exclude = ['waypoints', ]
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

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




class WaypointFormSet(forms.BaseModelFormSet):
    pass
