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
from .parsers import RailroadScheduleParser


class WaypointStationSubmitError(Exception):
    """Raised when submitted stations (departure station, arrival station) are identical.
    """


class RailroadSearchEngine:

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
        self._input_elements = None

    def start_engine(self):
        self._driver.get("https://portalpasazera.pl/Wyszukiwarka/Index")
        self._search_input_elements()
        return self

    def _search_input_elements(self):
        self._input_elements = {}

        elements = [
            ('departure_page_element', '//*[@id="departureFrom"]'),
            ('arrival_page_element', '//*[@id="arrivalTo"]'),
            ('date_page_element', '//*[@id="main-search__dateStart"]'),
            ('hour_page_element', '//*[@id="main-search__timeStart"]'),
            ('direct_btn_page_element', '//*[@id="dirChck"]'),
            ('enter_btn_page_element', '/html/body/div[6]/div/form/div[6]/div[1]/div[1]/div/div/input',)
        ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for name, xpath in elements:
                found_element = executor.submit(self._driver.find_element, By.XPATH, xpath)
                self._input_elements[name] = found_element.result()

        return self._input_elements

    def submit_stations(self, departure_station:str, arrival_station:str):
        if not self._input_elements:
            self._search_input_elements()

        if str(departure_station).lower() == str(arrival_station).lower():
            raise WaypointStationSubmitError(
                'departure station must be different than arrival station and vice versa.'
            )

        elements = [
            self._input_elements['departure_page_element'],
            self._input_elements['arrival_page_element'],
        ]

        for element, value in zip(elements, [departure_station, arrival_station]):
            element.send_keys(value)

    def submit_date(self, hour:str, date:str):
        if not self._input_elements:
            self._search_input_elements()

        if not search_engine_date_regex.match(str(date)):
            raise ValueError("invalid date provided; must be in pattern e.g. '12.11.2021' or 12-11-2021 ")

        if not hour_regex.match(str(hour)):
            raise ValueError("invalid hour provided; must be in pattern e.g. '21:37'")

        elements = [
            self._input_elements['hour_page_element'],
            self._input_elements['date_page_element'],
        ]

        for element, value in zip(elements, [hour, date]):
            element.clear()
            element.send_keys(value)

    def click_direct(self):
        if not self._input_elements:
            self._search_input_elements()

        direct_btn_page_element = self._input_elements['direct_btn_page_element']
        ActionChains(self._driver).move_to_element(direct_btn_page_element).perform()
        self._driver.execute_script("arguments[0].click();", direct_btn_page_element)

    def click_enter(self):
        if not self._input_elements:
            raise ValueError("cant click enter button; page elements must be found first.")

        element = self._input_elements['enter_btn_page_element']
        element.send_keys(Keys.ENTER)

    def await_schedule(self):
        timeout = 4
        wait = WebDriverWait(self._driver, timeout)
        xpath = '/html/body/div[6]/div[1]/div[1]/div[2]/h2'
        schedule_appearance = ec.presence_of_element_located((By.XPATH, xpath))
        return wait.until(schedule_appearance)

    def request_schedule_markup(self, departure_station, arrival_station, hour, date):
        if not self._input_elements:
            self._search_input_elements()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            submit_stations = executor.submit(self.submit_stations, departure_station, arrival_station)
            submit_date = executor.submit(self.submit_date, hour, date)

            for process in [submit_stations, submit_date]:
                process.result()

            click_enter = executor.submit(self.click_enter)
            click_direct = executor.submit(self.click_direct)

            for process in [click_enter, click_direct]:
                process.result()

        try:
            self.await_schedule()
        except TimeoutException as e:
            self._driver.quit()
            raise ValueError(f'{e.msg}: schedule has not appeared -  no markup returned.')

        markup = self._driver.page_source
        self._driver.quit()
        return markup

    def check_stations_existence(self, departure_station, arrival_station):
        """Verifies stations existence by submitting them to webpage fields and
        awaiting schedule appearance. When the schedule appears, the stations are correct, otherwise not.
        """
        self.start_engine()
        self._search_input_elements()
        self.submit_stations(departure_station, arrival_station)
        self.click_enter()

        try:
            self.await_schedule()
        except TimeoutException:
            self._driver.quit()
            return False
        else:
            return True

    def run_searching(self, departure_station, arrival_station, hour, date) -> dict:
        """Final function for searching trains using this engine,
        departure_station and arrival_station cannot be the same,
        time_start arg must be in given pattern, like '21:37',
        date_start arg also needs to be in pattern, e.g. '12.11.2021' or 12-11-2021,
        Returns list of dictionaries like:

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron III Tor 4'}, 'start_date': {'date': '23.11.2021', 'hour': '18:51'},
            'end_date': {'date': '23.11.2021', 'hour': '19:19'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'number': '40844'},

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron III Tor 2'}, 'start_date': {'date': '23.11.2021', 'hour': '19:16'},
            'end_date': {'date': '23.11.2021', 'hour': '19:45'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'number': '40634'},

            {'start_waypoint': {'station': 'Gliwice', 'platform': 'Peron II Tor 5'}, 'end_waypoint': {'station':
            'Katowice', 'platform': 'Peron IV Tor 10'}, 'start_date': {'date': '23.11.2021', 'hour': '19:32'},
            'end_date': {'date': '23.11.2021', 'hour': '19:56'}, 'carrier': '„PKP Intercity” Spółka Akcyjna',
            'number': '63102'}
        """
        self.start_engine()
        self._search_input_elements()

        schedule_markup = self.request_schedule_markup(
            departure_station, arrival_station, hour, date
        )
        parser = RailroadScheduleParser(schedule_markup)
        trains = parser.parse_schedule()

        return trains
