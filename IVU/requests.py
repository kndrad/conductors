from . import date_re, text_re, DateRegexError, TextRegexError
from .abstracts.requests import IVURequest


class IVUDatedRequest(IVURequest):
    fmt = '%Y-%m-%d'

    def __init__(self, date, *args, **kwargs):
        if not date_re.match(date):
            raise DateRegexError(date)
        super().__init__(*args, **kwargs)


class IVUTextRequest(IVURequest):
    def __init__(self, text, *args, **kwargs):
        if not text_re.match(text):
            raise TextRegexError(text)
        super().__init__(*args, **kwargs)
