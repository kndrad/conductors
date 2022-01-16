import abc

import caldav
from django.contrib import messages
from django.shortcuts import redirect


class CalDAVAccountDoesNotExist(Exception):
    pass


class CalDAVSendEventsMixin:
    request = None
    calendar = None

    @abc.abstractmethod
    def get_query_to_send(self):
        pass

    @abc.abstractmethod
    def final_redirect(self):
        pass

    @property
    @abc.abstractmethod
    def calendar_name(self):
        pass

    def post_events(self):
        self.save_events()

    def _dav_client(self):
        user = self.request.user
        account = 'caldav_account'

        if hasattr(user, account):
            return getattr(user, account).get_client()
        else:
            message = "Do wysyłania wydarzeń, potrzebna jest konfiguracja konta CalDAV."
            messages.error(self.request, message)
            raise CalDAVAccountDoesNotExist

    def get_dav_calendar(self, name):
        client = self._dav_client()
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

        for instance in self.get_query_to_send():
            ical = instance.ical_component().to_ical()
            self.calendar.save_event(ical)

    def save_other_events(self, other):
        for event in other:
            if event:
                ical = event.ical_component().to_ical()
                self.calendar.save_event(ical)

    def post(self, request, **kwargs):
        calendar_name = self.calendar_name()

        try:
            self.calendar = self.get_dav_calendar(name=calendar_name)
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
