"""
Django settings for ElexonDataManager project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import datetime as dt

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u8)g2o_8)3=ap4r9v4#x#1n4ucc!#*k$_$8=13-p$i0m$))!xs'

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
    'BMRA',
    'Physical'
    #'P114'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ElexonDataManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ElexonDataManager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ElexonData',
        'USER': 'ElexonData_django',
        'PASSWORD': '38f5414afd10bd1c1c9d3118367e60c2ad2692ae',
        'HOST': 'localhost',
        'PORT': '5432'
        }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Elexon values
ELEXON_BASEURL = 'https://downloads.elexonportal.co.uk/bmradataarchive/download'
ELEXON_KEY = '8bjll9hlkqh7gb8'
P114_LIST_URL = 'https://downloads.elexonportal.co.uk/p114/list?key={}&date={:04d}-{:02d}-{:02d}'
P114_DOWNLOAD_URL = 'https://downloads.elexonportal.co.uk/p114/download?key={}&filename={}'

# Local folders for file processing
BMRA_INPUT_DIR = '/home/graeme/ElexonData/Unprocessed/'
BMRA_PROCESSED_DIR = '/home/graeme/ElexonData/Processed/'
P114_INPUT_DIR = '/home/graeme/ElexonData/P114'

# Magic Numbers
#BMRA_START_DATE = dt.date(2002,1,1) #earliest date of BMRA data for validation
BMRA_DATA_START_DATE = dt.date(2002,1,1) #first date of data contents
BMRA_FILE_START_DATE = None #first date of data publication
P114_DATA_START_DATE = None #first date of P114 data contents
P114_FILE_START_DATE = dt.date(2010,4,1) #earliest date of P114 publication

# NETA downloads
NETA_USER = 'meepmeep' #NETA username
NETA_PWD = 'Bagp13net' #NETA password
NETA_BMU_LIST_URL = 'https://www.netareports.com/dataService?rt=bmunit&username={}&password={}' #url for NETA reports list of BMUs
