from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from alina.models import AllocationTimetable


class AllocationTimetableImportForm(forms.ModelForm):
    """Contains only month and year fields.
    Takes user instance in it's constructor to provide user initial value in this form field.
    """

    class Meta:
        model = AllocationTimetable
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
