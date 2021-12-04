import concurrent.futures

from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

from .expressions import (
    timeline_regex,
    start_container_selector_regex,
    end_container_selector_regex,
    time_container_selector_regex,
    hour_regex,
    overall_info_container_selector_regex,
    number_regex,
)


class RailroadScheduleRowParser:

    def __init__(self, row):
        self._markup = row

    def get_waypoint(self, timeline):
        if not timeline_regex.match(timeline):
            raise ValueError("unable to get location info; given timeline must be either 'start' or 'end'.")

        if timeline == 'start':
            timeline_container_element = start_container_selector_regex
        else:
            timeline_container_element = end_container_selector_regex

        tag = 'div'
        timeline_container = self._markup.find(name=tag, class_=timeline_container_element)

        tag = 'p'
        station_content_cls = 'timeline__content-station'
        station = timeline_container.find(name=tag, class_=station_content_cls)

        platform_content_cls = 'timeline__content-platform'
        platform = timeline_container.find(name=tag, class_=platform_content_cls)

        return {
            'station': station.text.strip(),
            'platform': platform.text.strip()
        }

    def get_date(self, timeline):
        if not timeline_regex.match(timeline):
            raise ValueError("unable to get date and time; given timeline must be either 'start' or 'end'.")

        if timeline == 'start':
            datetime_container = 'row grid-add-gutter-bottom search-results__item-times--start'
        else:
            datetime_container = 'row search-results__item-times--end'

        tag = 'div'
        container = self._markup.find(name=tag, class_=datetime_container)

        tag = 'span'
        date_container_cls = 'stime search-results__item-date'
        date = container.find(name=tag, class_=date_container_cls)
        time = container.find(name=tag, class_=time_container_selector_regex)

        return {
            'date': date.text.strip(),
            'hour': hour_regex.match(time.text.strip()).group()
        }

    def get_carrier(self):
        tag = 'div'
        overall_info_container = self._markup.find(name=tag, class_=overall_info_container_selector_regex)

        tag = 'p'
        carrier_container = 'item-label'
        container = overall_info_container.find(name=tag, class_=carrier_container)

        tag = 'span'
        attrs = {'lang': 'pl-PL'}
        carrier = container.find(name=tag, attrs=attrs)
        return carrier.text.strip()

    def get_train_number(self):
        tag = 'p'
        number_container_element = 'search-results__item-train-nr'
        number = self._markup.find(name=tag, class_=number_container_element)
        number = number_regex.search(number.text.strip()).group()
        return number

    def parse_row(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            start_waypoint = executor.submit(self.get_waypoint, 'start')
            end_waypoint = executor.submit(self.get_waypoint, 'end')
            start_date = executor.submit(self.get_date, 'start')
            end_date = executor.submit(self.get_date, 'end')
            carrier = executor.submit(self.get_carrier)
            number = executor.submit(self.get_train_number)

            result = {
                'carrier': carrier.result(),
                'number': number.result(),
                'start_waypoint': start_waypoint.result(),
                'end_waypoint': end_waypoint.result(),
                'start_date': start_date.result(),
                'end_date': end_date.result(),
            }
        return result


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
        rows = self.get_rows()
        trains = [
            RailroadScheduleRowParser(row).parse_row() for row in rows
        ]
        return [train for train in trains if train]
