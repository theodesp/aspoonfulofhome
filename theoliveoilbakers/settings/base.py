"""
Django settings for theoliveoilbakers project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from os.path import abspath, dirname, join
from django.utils.translation import ugettext_lazy as _

# Absolute filesystem path to the Django project directory:
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'no-secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']

ADMINS = (
     ('Theo', 'thdespou@hotmail.com'),
)

MANAGERS = ADMINS

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.contrib.wagtailsitemaps',
    'django_extensions',
    'djcelery',

    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'theoliveoilbakers.urls'
WSGI_APPLICATION = 'theoliveoilbakers.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

## SQLite (simplest install)
#DATABASES = {
    #'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': join(PROJECT_ROOT, 'db.sqlite3'),
    #}
#}

# Celery
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERY_TASK_SERIALIZER = ['json']
CELERY_ACCEPT_CONTENT = ['json']

CELERY_SEND_EVENTS = True


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Nicosia'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    ('en', _("English")),
    ('el', _("Greek")),
    ('es', _("Spanish")),
)

LOCALE_PATHS = (
    join(PROJECT_ROOT, 'locale'),
    )

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'


COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# Template configuration

from django.conf import global_settings

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

# Wagtail settings

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

WAGTAIL_SITE_NAME = "theoliveoilbakers"

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

# Use Elasticsearch as the search backend for extra performance and better search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/search/backends.html#elasticsearch-backend
#
# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
#         'INDEX': 'theoliveoilbakers',
#     },
# }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Whether to use face/feature detection to improve image cropping - requires OpenCV
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

