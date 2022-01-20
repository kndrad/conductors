from re import compile


class IVUServerError(Exception):
    pass


class IVUServerConnectionNotEstablishedError(IVUServerError):
    def __init__(self):
        super().__init__(
            'tried to request IVU server while connection is not established;'
            'please login first via username and password;'
        )


class IVUServerAuthenticationError(IVUServerError):
    pass


class RegexError(Exception):
    def __init__(self, value, message):
        super().__init__(f'{value} invalid pattern; {message};')


class DateRegexError(RegexError):
    def __init__(self, value):
        super().__init__(value, 'may be one of 2021-11-1, 2021-11-01, 2021-09-1, 2021-09-01')


class TextRegexError(RegexError):
    def __init__(self, value):
        super().__init__(value, 'please provide text-like value')


'''
Month cases:
    >>> date_re.match('2021-9-1')            # month is '9' string
    True
    >>> date_re.match('2021-09-1')           # month is '09 string 
    True

Day cases:
    >>> date_re.match('2021-11-1')           # day is '1' string
    True
    >>> date_re.match('2021-11-01')          # day is '01' string
    True 
'''

date_regex = compile('(?P<date>(19|20\d\d)[-\.](0[1-9]|[1-9]|1[012])[- \.](0[1-9]|[12][0-9]|3[01]|[1-9]))')
hour_regex = compile('(\d+:\d+)')
text_regex = compile('\w+')
