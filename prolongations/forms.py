from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import TicketProlongation


class TicketProlongationModelForm(forms.ModelForm):
    class Meta:
        model = TicketProlongation
        fields = '__all__'
        exclude = ('expiration_date',)
        widgets = {
            'user': forms.HiddenInput(),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Prolongata takiego biletu już istnieje.',
            }
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'
