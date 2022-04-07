"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2q%jv1+0e5@uv+5^9buk36o9q*ktuw9)7ftkcnk!cj1!ib3bht'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'sign',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',

    'django_apscheduler',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'debug_info_format': {
                'format': '%(asctime)s %(levelname)s %(message)s'
            },
            'warning_mail_error_format': {
                'format': '{asctime} {levelname} {message} {pathname}',
                'style': '{',  # задает форматир. для атрибута LogRecord {attrname} вместо %(attrname)s в строке формата
            },
            'error_crit_format': {
                'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
                'style': '{',
            },
            'general_security_format': {
                'format': '{asctime} {levelname} {module} {message}',
                'style': '{',
            },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug_info_format',
            'filters': ['require_debug_true'],
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'warning_mail_error_format',
            'filters': ['require_debug_true'],
        },
        'console_errors': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'error_crit_format',
            'filters': ['require_debug_true'],
        },
        'mail_admins_handler': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'warning_mail_error_format',
            'filters': ['require_debug_false'],
        },
        'file_general_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'general_security_format',
            'filters': ['require_debug_false'],
            'filename': BASE_DIR / 'logs_dir' / 'general.log',
        },
        'file_errors_handler': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'error_crit_format',
            'filename': BASE_DIR / 'logs_dir' / 'errors.log',
        },
        'file_security_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'general_security_format',
            'filename': BASE_DIR / 'logs_dir' / 'security.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_errors', 'file_general_handler'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file_errors_handler', 'mail_admins_handler'],
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_errors_handler', 'mail_admins_handler'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_errors_handler'],
            'propagate': True,
        },
        'django.db_backends': {
            'handlers': ['file_errors_handler'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file_security_handler'],
            'propagate': True,
        },
    }
}

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = 'projects-mail-sf@yandex.ru'  # здесь указываем свою почту, с которой будут отправляться письма

ADMINS = [
    ('Eugene', 'phantom-post@yandex.ru'),
    # список всех админов в формате ('имя', 'их почта')
]

SERVER_EMAIL = 'projects-mail-sf@yandex.ru'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news/'
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_FORMS = {'signup': 'sign.forms.BasicSignupForm'}
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[NewsPortal]'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'projects-mail-sf'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = 'pjitartcihmxvine'  # пароль от почты
EMAIL_USE_SSL = True

# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше,
# но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

# Настройки конфигурации Celery для исп. Redis

CELERY_BROKER_URL = 'redis://:Wzjcwh2Ifj4U5kKEETTZJpFOC7L9SzDM@redis-14383.c263.us-east-1-2.ec2.cloud.redislabs.com:14383/0'
CELERY_RESULT_BACKEND = 'redis://:Wzjcwh2Ifj4U5kKEETTZJpFOC7L9SzDM@redis-14383.c263.us-east-1-2.ec2.cloud.redislabs.com:14383/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),  # Указываем, куда будем сохранять кэшируемые файлы!
        # Не забываем создать папку cache_files внутри папки с manage.py!
    }
}