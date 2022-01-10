from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Timetable


class AllocationTimetableImportForm(forms.ModelForm):
    """Contains only month and year fields.
    Takes user instance in it's constructor to provide user initial value in this form field.
    """

    class Meta:
        model = Timetable
        fields = '__all__'
        exclude = ('last_updated',)
        widgets = {
            'user': forms.HiddenInput(),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Plan został już zaimportowany.',
            }
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'


