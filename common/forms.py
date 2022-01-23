from django import forms


class HiddenInputUserForm(forms.BaseForm):
    """ BaseForm that sets 'user' field to be hidden. Initial value is set to user in a request.
    """
    class Meta:
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user
