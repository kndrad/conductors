from abc import abstractmethod, ABC
import datetime
from re import compile

from dateutil.parser import parse as parse_date
from django.utils.timezone import make_aware

from IVU.api import text_regex, hour_regex, date_regex

info_cls = compile('^allocation-info ((?!comparison).)*$')
begin, end = 'begin', 'end'
timeline_re = compile(f'^({begin}|{end})')


class IVUContainerHTML(ABC):
    name: str = None
    attrs: dict = None

    def __init__(self, markup):
        self.markup = markup

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class IVUAllocationHTMLContainer(IVUContainerHTML):
    name = 'div'
    attrs = {'class': 'allocation-day click-area clickable'}

    def __init__(self, markup):
        super().__init__(markup)
        self._inner_markup = self.markup.find('div', class_=info_cls)

    def _get_title(self):
        value = self._inner_markup.find('div', class_='title-text').text.strip()
        title = text_regex.search(value).group()
        return title

    # def _get_signature(self):
    #     attr = 'data-allocationid'
    #     signature = self._inner_markup[attr]
    #     return signature

    def _get_hour(self, timeline):
        if not timeline_re.match(timeline):
            raise ValueError(f'{timeline} expression does not match {timeline_re}.')

        value = self._inner_markup.find('span', class_=f'time {timeline}').text.strip()
        return hour_regex.search(value).group()

    def _get_date(self):
        value = self.markup['data-date']
        return date_regex.search(value).group()

    def to_dict(self):
        try:
            date = self._get_date()
            start_date = make_aware(parse_date(f"{date} {self._get_hour('begin')}"))
            end_date = make_aware(parse_date(f"{date} {self._get_hour('end')}"))

            if start_date > end_date:
                end_date += datetime.timedelta(days=1)

            return {
                'title': self._get_title(),
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


class IVUTrainCrewMemberContainerHTML(IVUContainerHTML):
    name = 'div'
    attrs = {'class': 'crew-value'}

    def _get_column_value(self, name):
        attrs = {
            'class': 'crew-info-column',
            'title': name,
        }
        column = self.markup.find('li', attrs=attrs)
        value = column.find('span')
        return value

    def _get_person(self):
        name = self._get_column_value('Nazwa')
        return name.text

    def _get_phone_number(self):
        try:
            number = self._get_column_value('Numer telefonu')
        except AttributeError:
            return None
        else:
            return number.text

    def _get_profession(self):
        profession = self._get_column_value('Typ załogi')
        return profession.text

    def _get_location(self, location):
        location = self._get_column_value(location)
        return location.text

    def to_dict(self):
        try:
            return {
                'person': self._get_person().title(),
                'phone': self._get_phone_number(),
                'profession': self._get_profession(),
                'start_location': self._get_location('Lokalizacja początkowa i początkowa'),
                'end_location': self._get_location('Koniec i cel'),
            }
        except AttributeError:
            return
