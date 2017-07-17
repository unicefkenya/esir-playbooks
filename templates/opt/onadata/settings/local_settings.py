# get most settings from staging_example.py (which in turn, imports from
# settings.py)
from onadata.settings.common import *  # noqa
from urlparse import urljoin

# # # now override the settings which came from staging # # # #
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ pgsql_db }}',
        'USER': '{{ pgsql_user }}',
        'PASSWORD': '{{ pgsql_password }}',
        'HOST': '{{ pgsql_host }}',
    },
    {% if pgsql_replica1_host is defined %}
    'replica1': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '{{ pgsql_db }}',
        'USER': '{{ pgsql_user }}',
        'PASSWORD': '{{ pgsql_password }}',
        'HOST': '{{ pgsql_replica1_host }}',
    },
    {% endif %}
}

{% if pgsql_replica1_host is defined %}
SLAVE_DATABASES = ['replica1']
DATABASE_ROUTERS = ['multidb.PinningMasterSlaveRouter']
MULTIDB_PINNING_SECONDS = 10
{% else %}
SLAVE_DATABASES = []
{% endif %}

{% if kpi_formbuilder_url is defined %}
KPI_FORMBUILDER_URL = '{{ kpi_formbuilder_url }}'
{% endif %}

# Make a unique unique key just for testing, and don't share it with anybody.
SECRET_KEY = '{{ django_secret_key }}'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.DjangoModelPermissions'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'onadata.libs.authentication.DigestAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'onadata.libs.authentication.TempTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
}
OAUTH2_PROVIDER['AUTHORIZATION_CODE_EXPIRE_SECONDS'] = 600
BROKER_TRANSPORT = 'librabbitmq'
BROKER_URL = 'amqp://{{ rabbitmq_user }}:{{ rabbitmq_password }}@{{ rabbitmq_host }}:5672/'

TEMPLATE_OVERRIDE_ROOT_DIR = '{{ codebase_path }}/onadata/libs/custom_template'

if isinstance(TEMPLATE_OVERRIDE_ROOT_DIR, basestring):
        # site templates overrides
        TEMPLATES[0]['DIRS'] = [
            os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'templates'),
        ] + TEMPLATES[0]['DIRS']
        # site static files path
        STATICFILES_DIRS += (
            os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'static'),
        )

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = '{{ aws_access_key }}'
AWS_SECRET_ACCESS_KEY = '{{ aws_secret_key }}'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
DEFAULT_FROM_EMAIL = 'noreply+{{ nginx_server_name }}@ona.io'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

{% if is_aws %}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = '{{ s3_bucket }}'
AWS_DEFAULT_ACL = 'private'
AWS_S3_FILE_OVERWRITE = False
{% endif %}

ADMINS = (
{% for user, email in email_admins %}
    ('{{ user }}', '{{ email }}'),
{% endfor %}
)

DEBUG = {{ debug }}
TEMPLATES[0]['OPTIONS']['debug'] = False

ALLOWED_HOSTS = [
    "{{ ansible_ec2_public_hostname|default(ansible_hostname) }}",
    "{{ ansible_ec2_public_ipv4|default(ansible_default_ipv4.address) }}",
    "{{ ansible_ec2_local_hostname|default(ansible_hostname) }}",
    "{{ ansible_ec2_local_ipv4|default(ansible_default_ipv4.address) }}",
{% for host in nginx_server_names|list + allowed_host|list %}
    '{{ host }}',
{% endfor %}
]

# Cross Origin Requests (CORS)

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'localhost:4000',
    'localhost:8000',
    'localhost:8080',
{% for origin in cors_origin_whitelist %}
    '{{ origin }}',
{% endfor %}
)

CORS_EXPOSE_HEADERS = (
    'Content-Type', 'Location', 'WWW-Authenticate', 'Content-Language',
    'ETag', 'X-total')

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-csrf-token',
    'cache-control',
    'if-none-match'
)

# Google credentials
GOOGLE_SITE_VERIFICATION = '{{ google_site_verification }}'
GOOGLE_ANALYTICS_PROPERTY_ID = '{{ google_analytics_property_id }}'
GOOGLE_ANALYTICS_DOMAIN = '{{ nginx_server_name }}'

# Flags
TESTING_MODE = False

# Enketo settings
JWT_SECRET_KEY = '{{ jwt_secret_key }}'
JWT_ALGORITHM = 'HS256'
ENKETO_AUTH_COOKIE_DOMAIN = '{{ enketo_auth_cookie_domain }}'
ENKETO_CLIENT_LOGIN_URL = '{{ enketo_login_url }}'
ENKETO_URL = '{{ enketo_url }}'
ENKETO_API_SURVEY_PATH = '/api_v2/survey'
ENKETO_PREVIEW_URL = urljoin(ENKETO_URL, ENKETO_API_SURVEY_PATH + '/preview')
ENKETO_API_INSTANCE_IFRAME_URL = ENKETO_URL + 'api_v1/instance/iframe'
ENKETO_API_SALT = '{{ enketo_api_salt }}'
ENKETO_API_TOKEN = '{{ enketo_api_token }}'
if {{ enketo_offline }}:
    ENKETO_API_INSTANCE_IFRAME_URL = urljoin(
        ENKETO_URL, 'api_v2/instance/iframe')
    ENKETO_API_SURVEY_PATH = '/api_v2/survey'
    ENKETO_API_INSTANCE_PATH = '/api_v2/instance'
    ENKETO_PREVIEW_URL = urljoin(
        ENKETO_URL, ENKETO_API_SURVEY_PATH + '/preview')
    ENKETO_API_SURVEY_PATH = urljoin(
        ENKETO_URL, ENKETO_API_SURVEY_PATH + '/offline')

if {{ is_aws }}:
    # source http://dryan.me/articles/elb-django-allowed-hosts/
    # add ec2 private ip - ensures load balancer has access
    import requests
    EC2_PRIVATE_IP = None
    try:
        EC2_PRIVATE_IP = requests.get(
            'http://169.254.169.254/latest/meta-data/local-ipv4',
            timeout=0.01
        ).text
    except requests.exceptions.RequestException:
        pass

    if EC2_PRIVATE_IP:
        ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
else:
    MEDIA_URL = "https://{{ nginx_server_name }}/media/"
    MEDIA_ROOT = os.path.join('/', 'home', 'onadata', 'media/')

# Celery
CELERY_ROUTES = {
    'onadata.apps.api.tasks.publish_xlsform_async': {
        'queue': 'publish_xlsform'},
    'onadata.apps.viewer.tasks.create_xls_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_csv_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_kml_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_osm_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_zip_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_csv_zip_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_sav_zip_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_external_export': {'queue': 'exports'},
    'onadata.apps.viewer.tasks.create_google_sheet_export': {
        'queue': 'exports'},
    'google_export.tasks.call_google_sheet_service': {
        'queue': 'google_export'},
}

# Set Cache-Control: max-age={{ cache_control_max_age }} seconds
CACHE_MIXIN_SECONDS = {{ cache_control_max_age }}

OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth2_provider.Application"

INSTALLED_APPS = ("django.forms",) + INSTALLED_APPS
FORM_RENDERER = u'django.forms.renderers.TemplatesSetting'
APPS_DIR = True

# mainly for data submission attachments, the max size we can accept
DEFAULT_CONTENT_LENGTH = {{ odk_content_length }}

GOOGLE_STEP2_URI = "https://{{ nginx_server_name }}/gwelcome"
GOOGLE_OAUTH2_CLIENT_ID = "{{ google_client_id}}"
GOOGLE_OAUTH2_CLIENT_SECRET = "{{ google_client_secret }}"
GOOGLE_CLIENT_EMAIL = "{{ google_client_email }}"

TAGGIT_CASE_INSENSITIVE = False
STREAM_DATA = True

{% if memcache_uri is defined %}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': "{{ memcache_uri }}",
    }
}
{% endif %}

{% if include_google_export %}
INSTALLED_APPS = ("google_export",) + INSTALLED_APPS
GOOGLE_EXPORT = True
REST_SERVICES_TO_MODULES = {
    'google_sheets': 'google_export.service'
}
REST_SERVICES_TO_SERIALIZERS = {
    'google_sheets': 'google_export.serializer.GoogleSheetsSerializer'
}
CUSTOM_MAIN_URLS = {
    'google_export.urls'
}
{% endif %}

{% if include_tableau %}
INSTALLED_APPS = ("connector",) + INSTALLED_APPS
if CUSTOM_MAIN_URLS:
    CUSTOM_MAIN_URLS.add('connector.urls')
else:
    CUSTOM_MAIN_URLS = {
        'connector.urls'
    }
{% endif %}

MIDDLEWARE = (
    {% if pgsql_replica1_host is defined %}
    'multidb.middleware.PinningRouterMiddleware',
    {% endif %}
    'onadata.libs.profiling.sql.SqlTimingMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'onadata.libs.utils.middleware.LocaleMiddlewareWithTweaks',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'onadata.libs.utils.middleware.HTTPResponseNotAllowedMiddleware',
)
