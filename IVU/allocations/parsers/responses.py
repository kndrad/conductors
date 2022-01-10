from bs4.element import SoupStrainer
from re import compile
from IVU.abstracts.parsers.responses import IVURequestResponseContentParser
from IVU.allocations.parsers.containers import IVUAllocationHTMLContainer, IVUAllocationActionContainerHTML

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
            data = element['data-url']
            return id_re.search(data)['id']
        except AttributeError:
            return


class IVUAllocationActionsRequestResponseParser(IVURequestResponseContentParser):
    strainer = SoupStrainer(name='tbody')
    container = IVUAllocationActionContainerHTML
