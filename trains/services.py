import concurrent.futures
import os
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from .expressions import search_engine_date_regex, hour_regex
from .parsers import TrainScheduleParser


class SentExactStationsError(Exception):
    """Raised when submitted stations (departure station, arrival station) are identical.
    """


class SearchingTrainScheduleService:

    def __init__(self, hide_actions=True):
        options = Options()
        for argument in ['--disable-extensions', '--incognito', ]:
            options.add_argument(argument)
        options.headless = hide_actions

        service = Service(os.path.join(Path(__file__).resolve().parent, 'geckodriver'))

        self._driver = webdriver.Firefox(
            options=options,
            service=service
        )
        self._elements = None

    def start(self):
        self._driver.get("https://portalpasazera.pl/Wyszukiwarka/Index")
        self._find_page_elements()
        return self

    def stop(self):
        return self._driver.quit()

    def _find_page_elements(self):
        self._elements = {}

        elements = [
            ('departure', '//*[@id="departureFrom"]'),
            ('arrival', '//*[@id="arrivalTo"]'),
            ('date', '//*[@id="main-search__dateStart"]'),
            ('hour', '//*[@id="main-search__timeStart"]'),
            ('direct_btn', '//*[@id="dirChck"]'),
            ('enter_btn', '/html/body/div[6]/div/form/div[6]/div[1]/div[1]/div/div/input',)
        ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for name, xpath in elements:
                found_element = executor.submit(self._driver.find_element, By.XPATH, xpath)
                self._elements[name] = found_element.result()

        return self._elements

    def send_stations(self, departure_station: str, arrival_station: str):
        if not self._elements:
            self._elements = self._find_page_elements()

        if str(departure_station).lower() == str(arrival_station).lower():
            raise SentExactStationsError(
                'departure station must be different than arrival station and vice versa.'
            )

        elements = [
            self._elements['departure'],
            self._elements['arrival'],
        ]

        for element, value in zip(elements, [departure_station, arrival_station]):
            element.send_keys(value)

    def send_date(self, hour: str, date: str):
        if not self._elements:
            self._elements = self._find_page_elements()

        if not search_engine_date_regex.match(str(date)):
            raise ValueError("invalid date provided; must be in pattern e.g. '12.11.2021' or 12-11-2021 ")

        if not hour_regex.match(str(hour)):
            raise ValueError("invalid hour provided; must be in pattern e.g. '21:37'")

        elements = [
            self._elements['hour'],
            self._elements['date'],
        ]

        for element, value in zip(elements, [hour, date]):
            element.clear()
            element.send_keys(value)

    def click_direct(self):
        if not self._elements:
            self._find_page_elements()

        direct_btn = self._elements['direct_btn']
        ActionChains(self._driver).move_to_element(direct_btn).perform()
        self._driver.execute_script("arguments[0].click();", direct_btn)

    def click_enter(self):
        if not self._elements:
            raise ValueError("cant click enter button; page elements must be found first.")

        element = self._elements['enter_btn']
        element.send_keys(Keys.ENTER)

    def await_schedule(self):
        timeout = 8
        wait = WebDriverWait(self._driver, timeout)
        return wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[1]/div[1]/div[2]/h2')))

    def get_markup(self, date, hour, departure, arrival):
        if not self._elements:
            self._find_page_elements()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            submit_stations = executor.submit(self.send_stations, departure, arrival)
            submit_date = executor.submit(self.send_date, hour, date)

            for process in [submit_stations, submit_date]:
                process.result()

            click_enter = executor.submit(self.click_enter)
            click_direct = executor.submit(self.click_direct)

            for process in [click_enter, click_direct]:
                process.result()

        try:
            self.await_schedule()
        except TimeoutException as e:
            self.stop()
            raise ValueError(f'{e.msg}: schedule has not appeared -  no markup returned.')

        markup = self._driver.page_source
        self.stop()
        return markup

    def get_trains(self, date, hour, departure, arrival) -> dict:
        """Final function for searching trains using this engine,
        departure_station and arrival_station cannot be the same,
        time_start arg must be in given pattern, like '21:37',
        date_start arg also needs to be in pattern, e.g. '12.11.2021' or 12-11-2021,
        Returns list of dictionaries like:

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron III Tor 4'}, 'start_date': {'date': '23.11.2021', 'hour': '18:51'},
            'end_date': {'date': '23.11.2021', 'hour': '19:19'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'trip': '40844'},

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron III Tor 2'}, 'start_date': {'date': '23.11.2021', 'hour': '19:16'},
            'end_date': {'date': '23.11.2021', 'hour': '19:45'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'trip': '40634'},

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 5'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron IV Tor 10'}, 'start_date': {'date': '23.11.2021', 'hour': '19:32'},
            'end_date': {'date': '23.11.2021', 'hour': '19:56'}, 'carrier': '„PKP Intercity” Spółka Akcyjna',
            'trip': '63102'}
        """
        self.start()
        self._find_page_elements()

        markuo = self.get_markup(date, hour, departure, arrival)
        parser = TrainScheduleParser(markuo)
        trains = parser.parse_schedule()
        return trains


def stations_exist(departure, arrival):
    """Verifies stations existence by submitting them to webpage fields and
    awaiting schedule appearance. When the schedule appears, the stations are correct, otherwise not.
    """
    engine = SearchingTrainScheduleService(hide_actions=True)
    engine.start()
    engine.send_stations(departure, arrival)
    engine.click_enter()

    try:
        engine.await_schedule()
    except TimeoutException:
        engine.stop()
        return False
    else:
        return True
