from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from common.forms import HiddenInputUserForm
from IVU.timetables.models import Timetable


class ImportTimetableForm(HiddenInputUserForm, forms.ModelForm):
    """Contains only month and year fields.
    Takes user instance in it's constructor to provide user initial value in this form field.
    """

    class Meta(HiddenInputUserForm.Meta):
        model = Timetable
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Plan został już zaimportowany.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'


