from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8080'


try:
    from .local import *
except ImportError:
    pass
