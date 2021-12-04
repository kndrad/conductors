from allauth.account.forms import LoginForm


class TailwindLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget_attrs_class = 'w-full text-center rounded'
        self.fields['login'].widget.attrs['class'] = widget_attrs_class
        self.fields['password'].widget.attrs['class'] = widget_attrs_class
