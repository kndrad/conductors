import concurrent.futures
from abc import ABC

from bs4 import BeautifulSoup


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
