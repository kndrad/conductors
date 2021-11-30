import datetime
from collections import UserDict

REPRESENTATIVE_DATE_FORMAT = "%H:%M %d.%m.%Yr."


class YEARS:
    def __init__(
            self, first: int = datetime.datetime.now().year, last: int = datetime.datetime.now().year + 1
    ):
        if first > last:
            raise ValueError('first year cannot be greater than last year.')
        self._dict = UserDict({int(year): str(year) for year in range(abs(first), abs(last) + 1)})

    def items(self):
        return self._dict.items()
