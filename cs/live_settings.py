# -* - coding: utf-8 -*-
import os
ROOT_PATH = os.getcwd() + '/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ROOT_PATH + 'db.sqlite3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

STATIC_URL = 'http://localhost/static/'
UPLOAD_URL = 'http://localhost/media/upload/'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

