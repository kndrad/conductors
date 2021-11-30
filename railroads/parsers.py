import concurrent.futures

from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from .expressions import (
    timeline_regex, start_container_selector_regex, end_container_selector_regex, time_container_selector_regex,
    common_hour_regex,
    overall_info_container_selector_regex, common_num_regex,
)


class ScheduleRowMarkupParser:

    def __init__(self, row_markup):
        self._markup = row_markup

    def get_location_information(self, timeline):
        if not timeline_regex.match(timeline):
            raise ValueError("unable to get location info; given timeline must be either 'start' or 'end'.")

        if timeline == 'start':
            timeline_container_cls = start_container_selector_regex
        else:
            timeline_container_cls = end_container_selector_regex

        tag = 'div'
        timeline_start_container = self._markup.find(name=tag, class_=timeline_container_cls)

        tag = 'p'
        station_content_cls = 'timeline__content-station'
        station = timeline_start_container.find(name=tag, class_=station_content_cls)

        platform_content_cls = 'timeline__content-platform'
        platform = timeline_start_container.find(name=tag, class_=platform_content_cls)

        return {
            'station': station.text.strip(),
            'platform': platform.text.strip()
        }

    def get_datetime(self, timeline):
        if not timeline_regex.match(timeline):
            raise ValueError("unable to get date and time; given timeline must be either 'start' or 'end'.")

        if timeline == 'start':
            datetime_container_cls = 'row grid-add-gutter-bottom search-results__item-times--start'
        else:
            datetime_container_cls = 'row search-results__item-times--end'

        tag = 'div'
        datetime_container = self._markup.find(name=tag, class_=datetime_container_cls)

        tag = 'span'
        date_container_cls = 'stime search-results__item-date'
        date = datetime_container.find(name=tag, class_=date_container_cls)
        time = datetime_container.find(name=tag, class_=time_container_selector_regex)

        return {
            'date': date.text.strip(),
            'time': common_hour_regex.match(time.text.strip()).group()
        }

    def get_carrier(self):
        tag = 'div'
        overall_info_container = self._markup.find(name=tag, class_=overall_info_container_selector_regex)

        tag = 'p'
        carrier_container_cls = 'item-label'
        carrier_container = overall_info_container.find(name=tag, class_=carrier_container_cls)

        tag = 'span'
        attrs = {'lang': 'pl-PL'}
        carrier = carrier_container.find(name=tag, attrs=attrs)
        return carrier.text.strip()

    def get_train_number(self):
        tag = 'p'
        train_number_container_cls = 'search-results__item-train-nr'
        train_number = self._markup.find(name=tag, class_=train_number_container_cls)
        train_number = common_num_regex.search(train_number.text.strip()).group()
        return train_number

    def parse_row(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            parse_start_location = executor.submit(self.get_location_information, 'start')
            parse_end_location = executor.submit(self.get_location_information, 'end')
            parse_start_datetime = executor.submit(self.get_datetime, 'start')
            parse_end_datetime = executor.submit(self.get_datetime, 'end')
            parse_carrier = executor.submit(self.get_carrier)
            parse_train_number = executor.submit(self.get_train_number)

            parsed_row = {
                'start_location': parse_start_location.result(),
                'end_location': parse_end_location.result(),
                'start_datetime': parse_start_datetime.result(),
                'end_datetime': parse_end_datetime.result(),
                'carrier': parse_carrier.result(),
                'train_number': parse_train_number.result()
            }

        return parsed_row


class RailroadScheduleParser:

    def __init__(self, schedule_markup):
        self._markup = schedule_markup

        tag = 'div'
        rows_container_cls = 'search-results__container'
        soup_strainer = SoupStrainer(name=tag, class_=rows_container_cls)

        self._soup = BeautifulSoup(schedule_markup, features='html.parser', parse_only=soup_strainer)

    def get_rows(self):
        tag = 'div'
        row_cls = 'search-results__item row abt-focusable'
        rows = self._soup.find_all(name=tag, class_=row_cls)
        return rows

    def parse_schedule(self):
        rows_markup = self.get_rows()
        trains = [
            ScheduleRowMarkupParser(row_markup=row_markup).parse_row() for row_markup in rows_markup
        ]
        return trains
