# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pathlib import Path
import os

import django.contrib.auth

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tuez=%8$@01$6=@3_k!_7h-s3kuy*%&+jx6wporw53(hv5!3!a'
DEBUG = True #desarrollo
#DEBUG = False #produccion

ALLOWED_HOSTS = [] #todos los servidores

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appportafolio',
]
#puedes incluir cualquier modulo/app que tengamos
#se pone para que sepa donde esta cada modulo

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pportafolio.urls'
WSGI_APPLICATION = 'pportafolio.wsgi.application'

TEMPLATES = [
    {
        'BACKEND':'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates'),], #'DIRS': [],
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

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if DEBUG == False:
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR/ 'db.sqlite3',
        }
    }

#modo local de Windows
if DEBUG == True:
    print("*********************DESARROLLO EN LOCAL**************")
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'vportafolio',
            'USER': 'postgres',
            'PASSWORD': 'Adivinala1.',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)#

SITE_ID = 1
SITE_NAME = "Portfolio"
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#nuevo
TEMPLATE_CONTEXT_PROCESSORS = (
'django.contrib.auth.context_processors.auth',
    'djblets.siteconfig.context_processors.siteconfig',
    'djblets.util.context_processors.settingsVars',
    'djblets.util.context_processors.siteRoot',
    'djblets.util.context_processors.ajaxSerial',
    'djblets.util.context_processors.mediaSerial',
	'django.template.context_processors.request',)


#la parte estática es obligatoria para Heroku y para nuestra máquina
STATIC_URL = '/static/'    #js, css3, ..
MEDIA_ROOT = ''
MEDIA_URL = '/media/'  #videos, imágenes
STATIC_ROOT= os.path.join(BASE_DIR, 'static')
#os.path. --> para que sepa donde esta si en windows o linux, etc
#join para unir la ruta


# declara la ruta donde se enlazará el contenido estático
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
	('css', os.path.join(STATIC_ROOT, 'css')),
	('js', os.path.join(STATIC_ROOT, 'js')),
	('images', os.path.join(STATIC_ROOT, 'images')),
	'''('img', os.path.join(STATIC_ROOT, 'img')),'''
    #os.path.join(BASE_DIR, 'static'),
    #os.path.join(BASE_DIR, 'img'),
)

#CORREO ELECTRÓNICO
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ashleychuquitarco2@gmail.com' #emisor --> quien manda email
EMAIL_HOST_PASSWORD = 'cvbr zzxj rdqc aojz'
EMAIL_USE_TLS = True #seguridad de gmail

# List of finder classes that know how to find static files in
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
)
