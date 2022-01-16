from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile

sentence_validator = RegexValidator(
    _lazy_re_compile(r'^[a-zA-Z0-9äöüÄÖÜ]*$'),
    message='Wpisz poprawną nazwę',
    code='invalid',
)


def validate_sentence(value):
    return sentence_validator(value)
