from django.views.generic.edit import FormMixin


class HiddenUserFormMixin(FormMixin):
    """Updates form hidden input with a request user object.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'request'):
            kwargs.update({'user': self.request.user})
        return kwargs
