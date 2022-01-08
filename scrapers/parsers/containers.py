import abc

from scrapers.tools.expressions import (
    irena_date_regex, common_hour_regex, common_word_regex, allocation_information_container_regex,
    allocation_timeline_regex
)


class ContainerMarkupParser:
    """Subclasses must implement own set of methods to parse individual data.
    Usage of those methods is shown in parse_container method.
    """

    def __init__(self, container):
        self._container = container

    @abc.abstractmethod
    def parse_container(self) -> dict:
        """Returns parsed container data as a dictionary."""


class AllocationContainerMarkupParser(ContainerMarkupParser):

    def __init__(self, container):
        super().__init__(container)
        self._information_container = self._get_information_container()

    def _get_information_container(self):
        container = self._container.find('div', class_=allocation_information_container_regex)
        return container

    def _get_title(self):
        found_title = self._information_container.find('div', class_='title-text').text.strip()
        title = common_word_regex.search(found_title).group()
        return title

    def _get_signature(self):
        attribute = 'data-allocationid'
        allocatable_id = self._information_container[attribute]
        return allocatable_id

    def _get_hour(self, timeline):
        if not allocation_timeline_regex.match(timeline):
            raise ValueError(f'{timeline} expression does not match {allocation_timeline_regex}.')

        found_hour = self._information_container.find('span', class_=f'time {timeline}').text.strip()
        hour = common_hour_regex.search(found_hour).group()
        return hour

    def _get_date(self):
        attribute = 'data-date'
        found_date = self._container[attribute]
        date = irena_date_regex.search(found_date).group()
        return date

    def parse_container(self):
        """Returns allocation dict.
        """
        try:
            return {
                'title': self._get_title(),
                'signature': self._get_signature(),
                'date': self._get_date(),
                'start_hour': self._get_hour('begin'),
                'end_hour': self._get_hour('end')
            }
        except AttributeError:
            return


class AllocationDetailRowContainerMarkupParser(ContainerMarkupParser):

    def _get_cell_value(self, cell_class):
        cell = self._container.find('td', class_=cell_class)
        value = cell.find('span', class_='value').text.strip()
        return value

    def _get_train_number(self):
        train_number = self._get_cell_value('trip_numbers mdl-data-table__cell--non-numeric')
        return train_number

    def _get_action(self):
        action = self._get_cell_value('type_long_name mdl-data-table__cell--non-numeric')
        return action

    def _get_location(self, timeline):
        location = self._get_cell_value(f'{timeline}_location_long_name mdl-data-table__cell--non-numeric')
        return location

    def _get_date(self):
        pass

    def _get_hour(self, timeline):
        hour = self._get_cell_value(f'{timeline}_time mdl-data-table__cell--non-numeric')
        return hour

    def parse_container(self):
        """Returns detail dict from row container.
        """
        try:
            return {
                'train_number': self._get_train_number(),
                'action': self._get_action(),
                'start_location': self._get_location('start'),
                'start_hour': self._get_hour('start'),
                'end_location': self._get_location('end'),
                'end_hour': self._get_hour('end'),
            }
        except AttributeError:
            return


class CrewMemberContainerMarkupParser(ContainerMarkupParser):

    def _get_column_value(self, name):
        attrs = {
            'class': 'crew-info-column',
            'title': name,
        }
        column = self._container.find('li', attrs=attrs)
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

    def _get_start_location(self):
        location = self._get_column_value('Lokalizacja początkowa i początkowa')
        return location.text

    def _get_end_location(self):
        location = self._get_column_value('Koniec i cel')
        return location.text

    def parse_container(self):
        """Returns crew member dict.
        """
        try:
            return {
                'person': self._get_person().title(),
                'phone_number': self._get_phone_number(),
                'profession': self._get_profession(),
                'start_location': self._get_start_location(),
                'end_location': self._get_end_location(),
            }
        except AttributeError:
            return
