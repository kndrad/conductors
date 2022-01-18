from django.views.generic.edit import FormMixin
from .forms import HiddenInputUserForm


class HiddenInputUserFormMixin(FormMixin):

    def get_form_kwargs(self):
        if not issubclass(self.form_class, HiddenInputUserForm):
            raise AttributeError(
                f'to use {self.__class__.__name__}, '
                f'form class attr must be a subclass of {HiddenInputUserForm.__name__}'
            )
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'request'):
            kwargs.update({'user': self.request.user})
        return kwargs
