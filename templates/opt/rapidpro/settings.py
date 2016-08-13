# -----------------------------------------------------------------------------
# Sample RapidPro settings file, this should allow you to deploy RapidPro
# locally on a PostgreSQL database.
#
# The following are requirements:
#     - a postgreSQL database named 'temba', with a user name 'temba' and
#       password 'temba' (with postgis extensions installed)
#     - a redis instance listening on localhost
# -----------------------------------------------------------------------------

# import our default settings
from settings_common import *  # noqa
import logging  # noqa

# -----------------------------------------------------------------------------
# Used when creating callbacks for Twilio, Nexmo etc..
# -----------------------------------------------------------------------------
HOSTNAME = '{{ nginx_server_name }}'
TEMBA_HOST = '{{ nginx_server_name }}'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
# -----------------------------------------------------------------------------
# Redis & Cache Configuration (we expect a Redis instance on localhost)
# -----------------------------------------------------------------------------
REDIS_HOST = "127.0.0.1"
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "%s:%s:%s" % (REDIS_HOST, REDIS_PORT, REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

# -----------------------------------------------------------------------------
# Need a PostgreSQL database on localhost with postgis extension installed.
# -----------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ pgsql_db }}',
        'USER': '{{ pgsql_user }}',
        'PASSWORD': '{{ pgsql_password }}',
        'HOST': '{{ pgsql_host }}',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
        }
    }
}

# reuse our connections for up to 60 seconds
DATABASES['default']['CONN_MAX_AGE'] = 60
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

INTERNAL_IPS = ('127.0.0.1',)

# -----------------------------------------------------------------------------
# Load nose in development
# -----------------------------------------------------------------------------
# INSTALLED_APPS = INSTALLED_APPS + ('django_nose', 'storages', )
INSTALLED_APPS = INSTALLED_APPS + ('storages', )
# INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )

# -----------------------------------------------------------------------------
# In development, add in extra logging for exceptions and the debug toolbar
# -----------------------------------------------------------------------------
MIDDLEWARE_CLASSES = \
    ('temba.middleware.ExceptionMiddleware',) + MIDDLEWARE_CLASSES

# -----------------------------------------------------------------------------
# In development, perform background tasks in the web thread (synchronously)
# -----------------------------------------------------------------------------
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'redis'

ADMINS = (
            ('RapidPro', 'rapidpro@ona.io'),
)
MANAGERS = ADMINS

# -----------------------------------------------------------------------------
# set the mail settings, override these in your settings.py
# if your site was at http://temba.io, it might look like this:
# -----------------------------------------------------------------------------
EMAIL_HOST = '{{ aws_email_server }}'
EMAIL_HOST_USER = '{{ aws_email_username }}'
DEFAULT_FROM_EMAIL = 'rapidpro@ona.io'
EMAIL_HOST_PASSWORD = '{{ aws_email_password }}'
EMAIL_USE_TLS = True

# where recordings and exports are stored
# AWS_STORAGE_BUCKET_NAME = 'dl.temba.io'


######
# DANGER: only turn this on if you know what you are doing!
#         could cause messages to be sent to live customer aggregators
SEND_MESSAGES = True

######
# DANGER: only turn this on if you know what you are doing!
#         could cause external APIs to be called in test environment
SEND_WEBHOOKS = True

######
# DANGER: only turn this on if you know what you are doing!
#         could cause emails to be sent in test environment
SEND_EMAILS = True

# -----------------------------------------------------------------------------
# This setting throws an exception if a naive datetime is used anywhere.
# (they should always contain a timezone)
# -----------------------------------------------------------------------------
import warnings  # noqa
warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

# -----------------------------------------------------------------------------
# Make our sitestatic URL be our static URL on development
# -----------------------------------------------------------------------------
STATIC_URL = '/sitestatic/'
MEDIA_ROOT = os.path.join('/', 'home', 'rapidpro', 'media/')

# -----------------------------------------------------------------------------
# Branding Configuration
# -----------------------------------------------------------------------------
from django.utils.translation import ugettext_lazy as _  # noqa
BRANDING = {
    '{{ nginx_server_name }}': {
        'slug': 'rapidpro',
        'name': 'RapidPro',
        'org': 'UNICEF',
        'styles': ['brands/rapidpro/font/style.css',
                   'brands/rapidpro/less/style.less'],
        'welcome_topup': 1000,
        'email': 'join@rapidpro.ona.io',
        'support_email': 'support@rapidpro.ona.io',
        'link': 'https://{{ nginx_server_name }}',
        'api_link': 'https://{{ nginx_server_name }}',
        'docs_link': 'http://knowledge.rapidpro.io',
        'domain': '{{ nginx_server_name }}',
        'favico': 'brands/rapidpro/rapidpro.ico',
        'splash': '/brands/rapidpro/splash.jpg',
        'logo': '/brands/rapidpro/logo.png',
        'allow_signups': True,
        'welcome_packs': [dict(size=5000, name="Demo Account"),
                          dict(size=100000, name="UNICEF Account")],
        'description': _(
            "Visually build nationally scalable mobile applications from"
            " anywhere in the world."),
        'credits': _(
            "Copyright &copy; 2012-2015 UNICEF, Nyaruka. All Rights Reserved.")
    }
}
DEFAULT_BRAND = '{{ nginx_server_name }}'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'pycountry': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

TWITTER_API_KEY = '{{ twitter_api_key}}'
TWITTER_API_SECRET = '{{ twitter_api_secret}}'

MAGE_API_URL = '{{ mage_api_url }}'
MAGE_AUTH_TOKEN = '{{ temba_auth_token}}'
