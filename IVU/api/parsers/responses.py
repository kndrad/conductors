import concurrent.futures
from abc import ABC

from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from re import compile
from .containers import IVUAllocationHTMLContainer, IVUAllocationActionContainerHTML, IVUTrainCrewMemberContainerHTML


class IVURequestResponseContentParser(ABC):
    strainer = None
    container = None

    def __init__(self, response):
        self.soup = BeautifulSoup(
            markup=response.content,
            features='html.parser',
            parse_only=self.strainer
        )

    @property
    def containers(self):
        markups = self.soup.find_all(name=self.container.name, attrs=self.container.attrs)
        return [self.container(markup) for markup in markups]

    def perform(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [executor.submit(container.to_dict) for container in self.containers]
            results = [task.result() for task in tasks]

        return [result for result in results if result]


id_re = compile('(id=)(?P<id>\d+)')


class IVUTimetableAllocationsRequestResponseParser(IVURequestResponseContentParser):
    strainer = SoupStrainer(name='table', class_='duties calendar-table')
    container = IVUAllocationHTMLContainer


class IVUAllocationIDRequestResponseParser(IVURequestResponseContentParser):
    strainer = SoupStrainer(name='div', class_='allocation-container display-full')

    def get_containers(self):
        return

    def perform(self):
        try:
            element = self.soup.find(name='div', class_='clickable')
            return id_re.search(element['data-url'])['id']
        except AttributeError:
            return


class IVUAllocationActionsRequestResponseParser(IVURequestResponseContentParser):
    strainer = SoupStrainer(name='tbody')
    container = IVUAllocationActionContainerHTML


class IVUTrainCrewRequestResponseParser(IVURequestResponseContentParser):
    container = IVUTrainCrewMemberContainerHTML
