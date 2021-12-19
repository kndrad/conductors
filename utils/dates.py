import datetime
import enum
from collections import UserDict


class StringDateFormat(enum.Enum):
    FULL_DATE = "%H:%M %d.%m.%Yr."
    DATE_ONLY = "%d.%m.%Yr."
    TIME = "%H:%M"


class YEARS:
    def __init__(
            self, first: int = datetime.datetime.now().year, last: int = datetime.datetime.now().year + 1
    ):
        if first > last:
            raise ValueError('first year cannot be greater than last year.')
        self._dict = UserDict({int(year): str(year) for year in range(abs(first), abs(last) + 1)})

    def items(self):
        return self._dict.items()
