import os
from pathlib import Path

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DOMAIN_URL = os.getenv("BASE_DOMAIN_URL")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%%s3vg+wjn%7dk2ei!zl-e+zpo4q6!5cq@1m)*x$u8wcb(6b1v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    # our app
    "apps.common",
    "apps.blogs",
    "apps.groupdiscussions",
    "apps.payments",
    "apps.authentication",
    "apps.analytics",
    "apps.third_party_services",

    # third party
    'django_recaptcha',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'swabhyaas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.common.context_processor.common_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'swabhyaas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'apps.authentication.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

MESSAGE_TAGS = {
        messages.INFO: 'blue',
        messages.SUCCESS: 'green',
        messages.WARNING: 'teal',
        messages.ERROR: 'red',
 }

RECAPTCHA_PUBLIC_KEY = os.getenv("GOOGLE_RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("GOOGLE_RECAPTCHA_SECRET_KEY")

CKEDITOR_UPLOAD_PATH = "uploads/"

RAZORPAY_TEST_KEY = os.getenv("RAZORPAY_TEST_KEY")
RAZORPAY_TEST_SECRET_KEY = os.getenv("RAZORPAY_TEST_SECRET_KEY")
RAZORPAY_LIVE_KEY = os.getenv("RAZORPAY_LIVE_KEY")
RAZORPAY_LIVE_SECRET_KEY = os.getenv("RAZORPAY_LIVE_SECRET_KEY")

AUTH_MASTER_PASS=os.getenv("AUTH_MASTER_PASS")

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'youtube',
            ]),
    },
    "minimal": {
        "toolbar": "Custom",
        "extraPlugins": ",".join(["codesnippet", "youtube"]),
        "toolbar_YourCustomToolbarConfig": [
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Strike",
                    "-",
                    "Styles", 
                    "Format",
                    "Font", 
                    "FontSize",
                    "NumberedList",
                    "BulletedList",
                    "TextColor",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                ],
            },
            "/",
            {"name": "coderelated", "items": ["CodeSnippet", "Youtube"]},
        ],
        "toolbar": "YourCustomToolbarConfig",
        "removeDialogTabs": "image:advanced;image:Link",  # Remove 'Advanced' and 'Link' tabs from the 'Image' dialog.
        "image2_prefillDimensions": False,  # Ensures 'Upload' tab is focused by default.
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Zoom
ZOOM_ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")

#all auth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_ADAPTER = 'apps.authentication.custom_adapter.CustomAdapter'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv("OAUTH_CLIENT_ID"),
            'secret': os.getenv("OAUTH_CLIENT_SECRET"),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}