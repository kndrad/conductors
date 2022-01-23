import abc


class ICalConvertable:
    """ Intrerface for classes that implements a method that returns ical component.
    """
    @abc.abstractmethod
    def to_ical_component(self):
        pass
