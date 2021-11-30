class ExpressionPatternError(Exception):
    def __init__(self, expression, message):
        super().__init__(f'{expression} invalid pattern; {message};')


class DateExpressionPatternError(ExpressionPatternError):
    def __init__(self, expression):
        super().__init__(expression, ' may be one of 2021-11-1, 2021-11-01, 2021-09-1, 2021-09-01')


class TextExpressionPatternError(ExpressionPatternError):
    def __init__(self, expression):
        super().__init__(expression, 'please provide text-like expression')
