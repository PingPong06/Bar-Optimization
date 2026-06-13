from pathlib import Path
import os
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='cutflow-dev-secret-key-change-in-production-2026')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS', default='*' if DEBUG else '', cast=Csv()))

if not DEBUG:
    if SECRET_KEY.startswith('cutflow-dev-secret-key'):
        raise RuntimeError('SECRET_KEY must be set to a private value when DEBUG=False.')
    if not ALLOWED_HOSTS:
        raise RuntimeError('ALLOWED_HOSTS must be set when DEBUG=False.')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Internal apps
    'accounts',
    'catalog',
    'projects',
    'quotations',
    'production',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RoleMiddleware',
]

ROOT_URLCONF = 'CutFlow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.company_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'CutFlow.wsgi.application'

# Use SQLite for local development only. Production must use the configured database.
use_sqlite = config('USE_SQLITE', default=DEBUG, cast=bool)

if not use_sqlite:
    if DEBUG and config('DB_FALLBACK_TO_SQLITE', default=True, cast=bool):
        try:
            import MySQLdb
            conn = MySQLdb.connect(
                host=config('DB_HOST', default='localhost'),
                user=config('DB_USER', default='cutflow_user'),
                password=config('DB_PASSWORD', default=''),
                port=config('DB_PORT', default=3306, cast=int),
                connect_timeout=2,
            )
            conn.close()
        except Exception as e:
            print(f"WARNING: MySQL connection failed ({e}). Falling back to SQLite for development.")
            use_sqlite = True

if use_sqlite:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DB_NAME', default='cutflow_db'),
            'USER': config('DB_USER', default='cutflow_user'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Email
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@cutflow.com')

# Company defaults (overridden via DB CompanySettings)
COMPANY_NAME = config('COMPANY_NAME', default='CutFlow Fenestration')
COMPANY_ADDRESS = config('COMPANY_ADDRESS', default='')
COMPANY_PHONE = config('COMPANY_PHONE', default='')
COMPANY_EMAIL = config('COMPANY_EMAIL', default='')

# Production security. Keep SSL flags configurable for staging behind proxies.
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000 if not DEBUG else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=not DEBUG, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=not DEBUG, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_TRUSTED_ORIGINS = list(config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv()))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Optimization defaults
DEFAULT_BAR_LENGTH_MM = 6000
DEFAULT_KERF_MM = 5
DEFAULT_END_WASTE_MM = 10
MIN_REUSABLE_OFFCUT_MM = 300

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
}
