import abc

import caldav
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin


class CalDAVAccountDoesNotExist(Exception):
    pass


class SingleObjectCalDAVMixin(SingleObjectMixin):
    request = None
    calendar = None

    @abc.abstractmethod
    def get_saveable_queryset(self):
        pass

    @abc.abstractmethod
    def post_events(self):
        pass

    @abc.abstractmethod
    def final_redirect(self):
        pass

    def _get_davclient(self):
        user = self.request.user
        account_name = 'caldav_account'

        if hasattr(user, account_name):
            return getattr(user, account_name).get_client()
        else:
            message = "Do wysyłania wydarzeń, potrzebna jest konfiguracja konta CalDAV."
            messages.error(self.request, message)
            raise CalDAVAccountDoesNotExist

    def server_calendar(self, name):
        client = self._get_davclient()
        principal = client.principal()

        try:
            dav_calendar = principal.calendar(name=name)
        except caldav.error.NotFoundError:
            dav_calendar = principal.make_calendar(name=name)

        return dav_calendar

    def save_events(self):
        if not self.calendar:
            raise AttributeError('you need to get dav calendar first from server.')

        for event in self.calendar.events():
            event.delete()

        for instance in self.get_saveable_queryset():
            ical = instance.ical_component().to_ical()
            self.calendar.save_event(ical)

    def save_other_events(self, other):
        for event in other:
            if event:
                ical = event.ical_component().to_ical()
                self.calendar.save_event(ical)

    def post(self, request, **kwargs):
        self.object = self.get_object()

        try:
            self.calendar = self.server_calendar(self.object.calendar_name)
        except CalDAVAccountDoesNotExist:
            message = "Do wysyłania wydarzeń, potrzebna jest konfiguracja konta CalDAV."
            messages.error(self.request, message)
            return redirect(self.request.user.account_reverse('caldav'))
        except caldav.error.DAVError:
            message = "Wystąpił błąd podczas wysyłania kalendarza. Spróbuj jeszcze raz."
            messages.error(self.request, message)
        else:
            self.post_events()

        return self.final_redirect()
