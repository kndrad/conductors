from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from common.forms import HiddenInputUserForm
from .models import Prolongation


class ProlongationModelForm(HiddenInputUserForm, forms.ModelForm):
    class Meta(HiddenInputUserForm.Meta):
        model = Prolongation
        fields = '__all__'
        exclude = ('expiration_date',)

        widgets = HiddenInputUserForm.Meta.widgets
        widgets['last_renewal_date'] = forms.DateInput(attrs={'type': 'date'})

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Prolongata takiego biletu już istnieje.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded text-black mb-2 text-base'
