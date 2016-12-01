import os
from onadata.settings.common import *


LOCALE_PATHS= [os.path.join(PROJECT_ROOT,'locale'),]

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'
TEMPLATE_DEBUG = os.environ.get('TEMPLATE_DEBUG', 'True') == 'True'
TEMPLATE_STRING_IF_INVALID = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ pgsql_db }}',
        'USER': '{{ pgsql_user }}',
        'PASSWORD': '{{ pgsql_password }}',
        'HOST': '{{ pgsql_host }}',
    }
}

MONGO_DATABASE = {
    'HOST': os.environ.get('KOBOCAT_MONGO_HOST', 'localhost'),
    'PORT': int(os.environ.get('KOBOCAT_MONGO_PORT', 27017)),
    'NAME': os.environ.get('KOBOCAT_MONGO_NAME', 'formhub'),
    'USER': os.environ.get('KOBOCAT_MONGO_USER', ''),
    'PASSWORD': os.environ.get('KOBOCAT_MONGO_PASS', '')
}

BROKER_TRANSPORT = 'librabbitmq'
BROKER_URL = os.environ.get(
    'KOBOCAT_BROKER_URL', 'amqp://admin:admin@localhost:5672/')

try:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '{{ django_secret_key }}')
except KeyError:
    raise Exception('DJANGO_SECRET_KEY must be set in the environment.')

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(' ')

TESTING_MODE = False
# This trick works only when we run tests from the command line.
if len(sys.argv) >= 2 and (sys.argv[1] == "test"):
    raise Exception(
        "Testing destroys data and must NOT be run in a production "
        "environment. Please use a different settings file if you want to "
        "run tests."
    )
    TESTING_MODE = True
else:
    TESTING_MODE = False


MEDIA_URL= '/' + os.environ.get('KOBOCAT_MEDIA_URL', 'media').strip('/') + '/'
STATIC_URL = '/static/'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/login_redirect/'


if os.environ.get('KOBOCAT_ROOT_URI_PREFIX'):
    KOBOCAT_ROOT_URI_PREFIX= '/' + os.environ['KOBOCAT_ROOT_URI_PREFIX'].strip('/') + '/'
    MEDIA_URL= KOBOCAT_ROOT_URI_PREFIX + MEDIA_URL.lstrip('/')
    STATIC_URL= KOBOCAT_ROOT_URI_PREFIX + STATIC_URL.lstrip('/')
    LOGIN_URL= KOBOCAT_ROOT_URI_PREFIX + LOGIN_URL.lstrip('/')
    LOGIN_REDIRECT_URL= KOBOCAT_ROOT_URI_PREFIX + LOGIN_REDIRECT_URL.lstrip('/')

if TESTING_MODE:
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'test_media/')
    subprocess.call(["rm", "-r", MEDIA_ROOT])
    MONGO_DATABASE['NAME'] = "formhub_test"
    CELERY_ALWAYS_EAGER = True
    BROKER_BACKEND = 'memory'
    ENKETO_API_TOKEN = 'abc'
    #TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
else:
   MEDIA_ROOT = os.path.join("{{ system_user_home }}", 'media/')

if PRINT_EXCEPTION and DEBUG:
    MIDDLEWARE_CLASSES += ('utils.middleware.ExceptionLoggingMiddleware',)

# Clear out the test database
if TESTING_MODE:
    MONGO_DB.instances.drop()

# include the kobocat-template directory
TEMPLATE_OVERRIDE_ROOT_DIR = os.environ.get(
    'KOBOCAT_TEMPLATES_PATH',
    "{{ checkout_path }}/onadata/libs/custom_template"
)
TEMPLATE_DIRS = ( os.path.join(TEMPLATE_OVERRIDE_ROOT_DIR, 'templates'), ) + TEMPLATE_DIRS
STATICFILES_DIRS += ( os.path.join(TEMPLATE_OVERRIDE_ROOT_DIR, 'static'), )

KOBOFORM_SERVER=os.environ.get("KOBOFORM_SERVER", "{{ koboform_server }}")
KOBOFORM_SERVER_PORT=os.environ.get("KOBOFORM_SERVER_PORT", "80")
KOBOFORM_SERVER_PROTOCOL=os.environ.get("KOBOFORM_SERVER_PROTOCOL", "http")
KOBOFORM_LOGIN_AUTOREDIRECT=False
KOBOFORM_URL=os.environ.get("KOBOFORM_URL", "http://{{ koboform_server }}")

TEMPLATE_CONTEXT_PROCESSORS = (
    'onadata.koboform.context_processors.koboform_integration',
) + TEMPLATE_CONTEXT_PROCESSORS

MIDDLEWARE_CLASSES = ('onadata.koboform.redirect_middleware.ConditionalRedirects', ) + MIDDLEWARE_CLASSES

CSRF_COOKIE_DOMAIN = os.environ.get('CSRF_COOKIE_DOMAIN', None)

if CSRF_COOKIE_DOMAIN:
    SESSION_COOKIE_DOMAIN = CSRF_COOKIE_DOMAIN
    SESSION_COOKIE_NAME = 'kobonaut'

SESSION_SERIALIZER='django.contrib.sessions.serializers.JSONSerializer'

# for debugging
# print "KOBOFORM_URL=%s" % KOBOFORM_URL
# print "SECRET_KEY=%s" % SECRET_KEY
# print "CSRF_COOKIE_DOMAIN=%s " % CSRF_COOKIE_DOMAIN

# MongoDB - moved here from common.py
if MONGO_DATABASE.get('USER') and MONGO_DATABASE.get('PASSWORD'):
    MONGO_CONNECTION_URL = (
        "mongodb://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s") % MONGO_DATABASE
else:
    MONGO_CONNECTION_URL = "mongodb://%(HOST)s:%(PORT)s" % MONGO_DATABASE

MONGO_CONNECTION = MongoClient(
    MONGO_CONNECTION_URL, safe=True, j=True, tz_aware=True)
MONGO_DB = MONGO_CONNECTION[MONGO_DATABASE['NAME']]

# BEGIN external service integration codes
# AWS_ACCESS_KEY_ID = os.environ.get('KOBOCAT_AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('KOBOCAT_AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('KOBOCAT_AWS_STORAGE_BUCKET_NAME')
# AWS_DEFAULT_ACL = 'private'

GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get("GOOGLE_ANALYTICS_TOKEN", False)
GOOGLE_ANALYTICS_DOMAIN = "auto"
# END external service integration codes

# If not properly overridden, leave uninitialized so Django can set the default.
# (see https://docs.djangoproject.com/en/1.8/ref/settings/#default-file-storage)
if os.environ.get('KOBOCAT_DEFAULT_FILE_STORAGE'):
    DEFAULT_FILE_STORAGE = os.environ.get('KOBOCAT_DEFAULT_FILE_STORAGE')

{% if aws_access_key is defined and aws_secret_key is defined %}
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = '{{ aws_access_key }}'
AWS_SECRET_ACCESS_KEY = '{{ aws_secret_key }}'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = 'noreply+{{ nginx_server_name }}@ona.io'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
{% endif %}

# EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND',
#     'django.core.mail.backends.filebased.EmailBackend')

# if EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
#     EMAIL_FILE_PATH = os.environ.get(
#         'EMAIL_FILE_PATH', os.path.join(PROJECT_ROOT, 'emails'))
#     if not os.path.isdir(EMAIL_FILE_PATH):
#         os.mkdir(EMAIL_FILE_PATH)

# Optional Sentry configuration: if desired, be sure to install Raven and set
# RAVEN_DSN in the environment
if 'RAVEN_DSN' in os.environ:
    try:
        import raven
    except ImportError:
        print 'Please install Raven to enable Sentry logging.'
    else:
        INSTALLED_APPS = INSTALLED_APPS + (
            'raven.contrib.django.raven_compat',
        )
        RAVEN_CONFIG = {
            'dsn': os.environ['RAVEN_DSN'],
        }
        try:
            RAVEN_CONFIG['release'] = raven.fetch_git_sha(BASE_DIR)
        except raven.exceptions.InvalidGitRepository:
            pass

POSTGIS_VERSION = (2, 1, 2)

# Enketo URL.
# Configurable settings.
ENKETO_URL = os.environ.get('ENKETO_URL', '{{ enketo_server }}')
ENKETO_URL= ENKETO_URL.rstrip('/')
ENKETO_API_TOKEN = os.environ.get('ENKETO_API_TOKEN', '{{ enketo_api_token }}')
ENKETO_VERSION= os.environ.get('ENKETO_VERSION', 'express').lower()
assert ENKETO_VERSION in ['legacy', 'express']
# Constants.
ENKETO_API_ENDPOINT_ONLINE_SURVEYS = '/survey'
ENKETO_API_ENDPOINT_OFFLINE_SURVEYS = '/survey/offline'
ENKETO_API_ENDPOINT_INSTANCE= '/instance'
ENKETO_API_ENDPOINT_INSTANCE_IFRAME= '/instance/iframe'
# Computed settings.
if ENKETO_VERSION == 'express':
    ENKETO_API_ROOT= '/api/v2'
    ENKETO_OFFLINE_SURVEYS= os.environ.get('ENKETO_OFFLINE_SURVEYS', 'True').lower() == 'true'
    ENKETO_API_ENDPOINT_PREVIEW= '/preview'
    ENKETO_API_ENDPOINT_SURVEYS= ENKETO_API_ENDPOINT_OFFLINE_SURVEYS if ENKETO_OFFLINE_SURVEYS \
            else ENKETO_API_ENDPOINT_ONLINE_SURVEYS
else:
    ENKETO_API_ROOT= '/api_v1'
    ENKETO_API_ENDPOINT_PREVIEW= '/webform/preview'
    ENKETO_OFFLINE_SURVEYS= False
    ENKETO_API_ENDPOINT_SURVEYS= ENKETO_API_ENDPOINT_ONLINE_SURVEYS
ENKETO_API_SURVEY_PATH = ENKETO_API_ROOT + ENKETO_API_ENDPOINT_SURVEYS
ENKETO_API_INSTANCE_PATH = ENKETO_API_ROOT + ENKETO_API_ENDPOINT_INSTANCE
ENKETO_PREVIEW_URL = ENKETO_URL + ENKETO_API_ENDPOINT_PREVIEW
ENKETO_API_INSTANCE_IFRAME_URL = ENKETO_URL + ENKETO_API_ROOT + ENKETO_API_ENDPOINT_INSTANCE_IFRAME

KPI_URL = os.environ.get('KPI_URL', False)

# specifically for site urls sent to enketo for form retrieval
ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'http')

INSTALLED_APPS = ("connector",) + INSTALLED_APPS

CUSTOM_MAIN_URLS = {
    'connector.urls'
}
