from conductors.settings.production import *

DEBUG = True

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
