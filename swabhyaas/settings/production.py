from .base import *
from colorama import Fore, Style

DEBUG = False
print(Fore.CYAN + "DEBUG is " + Fore.GREEN + str(DEBUG) + Style.RESET_ALL)

ALLOWED_HOSTS = ['swabhyaas.com','www.swabhyaas.com','127.0.0.1']

INSTALLED_APPS += ["anymail","storages",]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

MIDDLEWARE += ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware',]

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

DEFAULT_FROM_EMAIL = "support@swabhyaas.com"
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
ANYMAIL = {
"SENDINBLUE_API_KEY": os.getenv("BREVO_SECRET_API_KEY")
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.getenv("CLOUDFRONT_DOMAIN")

AWS_LOCATION = 'static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
#Note : We need to have an Origin access identity and let aws cloudfront update bucket policy

#For Media files:
DEFAULT_FILE_STORAGE = 'swabhyaas.storage_backends.MediaStorage' #the media storage configurations

ROLLBAR = {
    "access_token": os.getenv("ROLLBAR_ACCESS_TOKEN"),
    "environment": "production",
    "branch": "master",
    "root": BASE_DIR,
    "patch_debugview": False,
}

if os.getenv("FORCED_HTTPS"):
    SECURE_SSL_REDIRECT = True