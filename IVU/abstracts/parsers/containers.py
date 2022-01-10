from abc import abstractmethod, ABC


class IVUContainerHTML(ABC):
    name: str = None
    attrs: dict = None

    def __init__(self, markup):
        self.markup = markup

    @abstractmethod
    def to_dict(self) -> dict:
        pass
