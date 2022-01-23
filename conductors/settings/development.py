from conductors.settings.production import *


ALLOWED_HOSTS = [
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG = True

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
