from allauth.account.forms import LoginForm


class RoundedFieldsLoginForm(LoginForm):
    """Login form which shows rounded fields in html.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full rounded'
