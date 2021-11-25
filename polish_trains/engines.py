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

from polish_trains.parsers import TrainScheduleMarkupParser
from polish_trains.expressions import website_date_pattern, time_pattern


class IdenticalStationsSubmitError(Exception):
    """Raised when submitted stations (departure station, arrival station) are identical.
    """


class PolishTrainsSearchEngine:

    def __init__(self):
        options = Options()
        for argument in ['--disable-extensions', '--incognito', ]:
            options.add_argument(argument)
        options.headless = True

        service = Service(os.path.join(Path(__file__).resolve().parent, 'geckodriver'))

        self._driver = webdriver.Firefox(
            options=options,
            service=service
        )
        self._found_page_elements = None
        self._webpage_opened = False

    def open_webpage(self):
        self._driver.get("https://portalpasazera.pl/Wyszukiwarka/Index")
        self._webpage_opened = True

    def find_page_elements(self):
        if not self._webpage_opened:
            self.open_webpage()

        self._found_page_elements = dict()
        page_elements = [
            ('departure_page_element', '//*[@id="departureFrom"]'),
            ('arrival_page_element', '//*[@id="arrivalTo"]'),
            ('date_start_page_element', '//*[@id="main-search__dateStart"]'),
            ('time_start_page_element', '//*[@id="main-search__timeStart"]'),
            ('direct_btn_page_element', '//*[@id="dirChck"]'),
            ('enter_btn_page_element', '/html/body/div[6]/div/form/div[6]/div[1]/div[1]/div/div/input',)
        ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for page_element_name, xpath in page_elements:
                find_page_element_process = executor.submit(self._driver.find_element, By.XPATH, xpath)
                self._found_page_elements[page_element_name] = find_page_element_process.result()

        return self._found_page_elements

    def submit_stations(self, departure_station, arrival_station):
        if not self._found_page_elements:
            self.find_page_elements()

        if departure_station == arrival_station:
            raise IdenticalStationsSubmitError('departure station must be different than arrival station.')

        station_page_elements = [
            self._found_page_elements['departure_page_element'],
            self._found_page_elements['arrival_page_element'],
        ]

        for station_page_element, submit_value in zip(station_page_elements, [departure_station, arrival_station]):
            station_page_element.send_keys(submit_value.title())

    def submit_dates(self, time_start, date_start):
        if not self._found_page_elements:
            self.find_page_elements()

        if not website_date_pattern.match(date_start):
            raise ValueError("invalid date provided; must be in pattern e.g. '12.11.2021' or 12-11-2021 ")

        if not time_pattern.match(time_start):
            raise ValueError("invalid time provided; must be in pattern e.g. '21:31'")

        date_page_elements = [
            self._found_page_elements['time_start_page_element'],
            self._found_page_elements['date_start_page_element'],
        ]

        for date_page_element, submit_value in zip(date_page_elements, [time_start, date_start]):
            date_page_element.send_keys(submit_value)

    def click_direct_btn(self):
        if not self._found_page_elements:
            self.find_page_elements()

        direct_btn_page_element = self._found_page_elements['direct_btn_page_element']
        ActionChains(self._driver).move_to_element(direct_btn_page_element).perform()
        self._driver.execute_script("arguments[0].click();", direct_btn_page_element)

    def click_enter_btn(self):
        if not self._found_page_elements:
            raise ValueError("cant click enter button; page elements must be found first.")

        enter_btn_page_element = self._found_page_elements['enter_btn_page_element']
        enter_btn_page_element.send_keys(Keys.ENTER)

    def await_schedule(self):
        timeout = 10
        wait = WebDriverWait(self._driver, timeout)
        xpath = '/html/body/div[6]/div[1]/div[1]/div[2]/h2'
        schedule_presence = ec.presence_of_element_located((By.XPATH, xpath))
        return wait.until(schedule_presence)

    def request_schedule_markup(self, departure_station, arrival_station, time_start, date_start):
        if not self._found_page_elements:
            self.find_page_elements()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            submit_stations_process = executor.submit(self.submit_stations, departure_station, arrival_station)
            submit_date_process = executor.submit(self.submit_dates, time_start, date_start)
            for process in [
                submit_stations_process, submit_date_process
            ]:
                process.result()

            click_enter_btn_process = executor.submit(self.click_enter_btn)
            click_direct_btn_process = executor.submit(self.click_direct_btn)

            for process in [
                click_enter_btn_process, click_direct_btn_process
            ]:
                process.result()

        try:
            self.await_schedule()
        except TimeoutException:
            self._driver.quit()
            raise ValueError("schedule has not appeared.")
        else:
            markup = self._driver.page_source
            self._driver.quit()
            return markup

    def use_engine(self, departure_station, arrival_station, time_start, date_start) -> dict:
        """Final function for searching trains using this engine,
        departure_station and arrival_station cannot be the same,
        time_start arg must be in given pattern, like '21:37',
        date_start arg also needs to be in pattern, e.g. '12.11.2021' or 12-11-2021,
        Returns list of dictionaries like:

            {'start_location': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_location': {'station':
            'Katowice', 'platform': 'Peron III Tor 4'}, 'start_datetime': {'date': '23.11.2021', 'time': '18:51'},
            'end_datetime': {'date': '23.11.2021', 'time': '19:19'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'train_number': '40844'},

            {'start_location': {'station': 'Gliwice', 'platform': 'Peron II Tor 6'}, 'end_location': {'station':
            'Katowice', 'platform': 'Peron III Tor 2'}, 'start_datetime': {'date': '23.11.2021', 'time': '19:16'},
            'end_datetime': {'date': '23.11.2021', 'time': '19:45'}, 'carrier': 'Koleje Śląskie sp. z o.o.',
            'train_number': '40634'},

            {'start_location': {'station': 'Gliwice', 'platform': 'Peron II Tor 5'}, 'end_location': {'station':
            'Katowice', 'platform': 'Peron IV Tor 10'}, 'start_datetime': {'date': '23.11.2021', 'time': '19:32'},
            'end_datetime': {'date': '23.11.2021', 'time': '19:56'}, 'carrier': '„PKP Intercity” Spółka Akcyjna',
            'train_number': '63102'}
        """
        self.open_webpage()
        self.find_page_elements()
        schedule_markup = self.request_schedule_markup(
            departure_station, arrival_station, time_start, date_start
        )
        parser = TrainScheduleMarkupParser(schedule_markup)
        trains = parser.parse_schedule()
        return trains
