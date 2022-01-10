import datetime
from re import compile

from dateutil import parser as date_parser

from IVU import text_re, hour_re, date_re
from IVU.abstracts.parsers.containers import IVUContainerHTML

info_cls = compile('^allocation-info ((?!comparison).)*$')
timeline_re = compile("^('begin'|'end')")


class IVUAllocationHTMLContainer(IVUContainerHTML):
    name = 'div'
    attrs = {'class': 'allocation-day click-area clickable'}

    def __init__(self, markup):
        super().__init__(markup)
        self._inner_markup = self.markup.find('div', class_=info_cls)

    def _get_title(self):
        value = self._inner_markup.find('div', class_='title-text').text.strip()
        title = text_re.search(value).group()
        return title

    def _get_signature(self):
        attr = 'data-allocationid'
        signature = self._inner_markup[attr]
        return signature

    def _get_hour(self, timeline):
        if not timeline_re.match(timeline):
            raise ValueError(f'{timeline} expression does not match {timeline_re}.')

        value = self._inner_markup.find('span', class_=f'time {timeline}').text.strip()
        hour = hour_re.search(value).group()
        return hour

    def _get_date(self):
        value = self.markup['data-date']
        return date_re.search(value).group()

    def to_dict(self):
        try:
            date = self._get_date()
            start_date = date_parser(f"{date} {self._get_hour('begin')}")
            end_date = date_parser(f"{date} {self._get_hour('end')}")

            if start_date < end_date:
                end_date += datetime.timedelta(days=1)

            return {
                'title': self._get_title(),
                'signature': self._get_signature(),
                'start_date': start_date,
                'end_date': end_date,
            }
        except AttributeError:
            return


class IVUAllocationActionContainerHTML(IVUContainerHTML):
    name = 'tr'
    attrs = {'class': compile('^(duty-components).*')}

    def __get_text(self, cls):
        cell = self.markup.find('td', class_=cls)
        return cell.find('span', class_='value').text.strip()

    def _get_train_number(self):
        return self.__get_text('trip_numbers mdl-data-table__cell--non-numeric')

    def _get_name(self):
        return self.__get_text('type_long_name mdl-data-table__cell--non-numeric')

    def _get_location(self, timeline):
        return self.__get_text(f'{timeline}_location_long_name mdl-data-table__cell--non-numeric')

    def _get_hour(self, timeline):
        return self.__get_text(f'{timeline}_time mdl-data-table__cell--non-numeric')

    def to_dict(self):
        try:
            return {
                'train_number': self._get_train_number(),
                'name': self._get_name(),
                'start_location': self._get_location('start'),
                'start_hour': self._get_hour('start'),
                'end_location': self._get_location('end'),
                'end_hour': self._get_hour('end'),
            }
        except AttributeError:
            return
