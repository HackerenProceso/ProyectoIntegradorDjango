"""
Django settings for Core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
# Configuración de Simple JWT
from datetime import timedelta
# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

#ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'mitiendita.fun,127.0.0.1,0.0.0.0,localhost,app-a39q2.ondigitalocean.app').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Theme
    'dashboards.apps.DashboardsConfig',
    'auth.apps.AuthConfig',
    
    #Api
    'rest_framework',
    'rest_framework_simplejwt',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #API 
    'corsheaders.middleware.CorsMiddleware',
]

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True  # Permitir acceso desde cualquier origen

# O permitir solo ciertos orígenes (más seguro)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # Origen de tu aplicación web
#     "https://your-frontend-domain.com",
#     "myapp://localhost",  # Origen de tu aplicación móvil
# ]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'origin',
    'x-csrftoken',
    'x-requested-with',
]

# Configuración de REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}


ROOT_URLCONF = 'Core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '_templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'theme': 'Core.templatetags.theme',
            },
            'builtins': [
                'django.templatetags.static',
                'Core.templatetags.theme',
            ]
        },
    },
]

WSGI_APPLICATION = 'Core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'u248345608_TECSUP'),
        'USER': os.getenv('DB_USER', 'u248345608_TECSUPMT'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'Tecsup.FINAL.1234.HOLA'),
        'HOST': os.getenv('DB_HOST', 'srv586.hstgr.io'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'assets/'

STATICFILES_DIRS = [
    BASE_DIR / 'assets',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#MEDIA_ROOT = os.path.join(BASE_DIR, 'assets/uploads')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


######################
# Keenthemes Settings
######################

KT_THEME = 'metronic'


# Theme layout templates directory

KT_THEME_LAYOUT_DIR = 'layout'


# Theme Mode
# Value: light | dark | system

KT_THEME_MODE_DEFAULT = 'light'
KT_THEME_MODE_SWITCH_ENABLED = True


# Theme Direction
# Value: ltr | rtl

KT_THEME_DIRECTION = 'ltr'


# Keenicons
# Value: duotone | outline | bold

KT_THEME_ICONS = 'duotone'


# Theme Assets

KT_THEME_ASSETS = {
    "favicon": "media/logos/favicon.ico",
    "fonts": [
        'https://fonts.googleapis.com/css?family=Inter:300,400,500,600,700',
    ],
    "css": [
        "plugins/global/plugins.bundle.css",
        "css/style.bundle.css"
    ],
    "js": [
        "plugins/global/plugins.bundle.js",
        "js/scripts.bundle.js",
    ]
}


# Theme Vendors

KT_THEME_VENDORS = {
    "datatables": {
        "css": [
            "plugins/custom/datatables/datatables.bundle.css"
        ],
        "js": [
            "plugins/custom/datatables/datatables.bundle.js"
        ]
    },
    "formrepeater": {
        "js": [
            "plugins/custom/formrepeater/formrepeater.bundle.js"
        ]
    },
    "fullcalendar": {
        "css": [
            "plugins/custom/fullcalendar/fullcalendar.bundle.css"
        ],
        "js": [
            "plugins/custom/fullcalendar/fullcalendar.bundle.js"
        ]
    },
    "flotcharts": {
        "js": [
            "plugins/custom/flotcharts/flotcharts.bundle.js"
        ]
    },
    "google-jsapi": {
        "js": [
            "//www.google.com/jsapi"
        ]
    },
    "tinymce": {
        "js": [
            "plugins/custom/tinymce/tinymce.bundle.js"
        ]
    },
    "ckeditor-classic": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-classic.bundle.js"
        ]
    },
    "ckeditor-inline": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-inline.bundle.js"
        ]
    },
    "ckeditor-balloon": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-balloon.bundle.js"
        ]
    },
    "ckeditor-balloon-block": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-balloon-block.bundle.js"
        ]
    },
    "ckeditor-document": {
        "js": [
            "plugins/custom/ckeditor/ckeditor-document.bundle.js"
        ]
    },
    "draggable": {
        "js": [
            "plugins/custom/draggable/draggable.bundle.js"
        ]
    },
    "fslightbox": {
        "js": [
            "plugins/custom/fslightbox/fslightbox.bundle.js"
        ]
    },
    "jkanban": {
        "css": [
            "plugins/custom/jkanban/jkanban.bundle.css"
        ],
        "js": [
            "plugins/custom/jkanban/jkanban.bundle.js"
        ]
    },
    "typedjs": {
        "js": [
            "plugins/custom/typedjs/typedjs.bundle.js"
        ]
    },
    "cookiealert": {
        "css": [
            "plugins/custom/cookiealert/cookiealert.bundle.css"
        ],
        "js": [
            "plugins/custom/cookiealert/cookiealert.bundle.js"
        ]
    },
    "cropper": {
        "css": [
            "plugins/custom/cropper/cropper.bundle.css"
        ],
        "js": [
            "plugins/custom/cropper/cropper.bundle.js"
        ]
    },
    "vis-timeline": {
        "css": [
            "plugins/custom/vis-timeline/vis-timeline.bundle.css"
        ],
        "js": [
            "plugins/custom/vis-timeline/vis-timeline.bundle.js"
        ]
    },
    "jstree": {
        "css": [
            "plugins/custom/jstree/jstree.bundle.css"
        ],
        "js": [
            "plugins/custom/jstree/jstree.bundle.js"
        ]
    },
    "prismjs": {
        "css": [
            "plugins/custom/prismjs/prismjs.bundle.css"
        ],
        "js": [
            "plugins/custom/prismjs/prismjs.bundle.js"
        ]
    },
    "leaflet": {
        "css": [
            "plugins/custom/leaflet/leaflet.bundle.css"
        ],
        "js": [
            "plugins/custom/leaflet/leaflet.bundle.js"
        ]
    },
    "amcharts": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/xy.js",
            "https://cdn.amcharts.com/lib/5/percent.js",
            "https://cdn.amcharts.com/lib/5/radar.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "amcharts-maps": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/map.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/continentsLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/usaLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldTimeZonesLow.js",
            "https://cdn.amcharts.com/lib/5/geodata/worldTimeZoneAreasLow.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "amcharts-stock": {
        "js": [
            "https://cdn.amcharts.com/lib/5/index.js",
            "https://cdn.amcharts.com/lib/5/xy.js",
            "https://cdn.amcharts.com/lib/5/themes/Animated.js"
        ]
    },
    "bootstrap-select": {
        "css": [
            "plugins/custom/bootstrap-select/bootstrap-select.bundle.css"
        ],
        "js": [
            "plugins/custom/bootstrap-select/bootstrap-select.bundle.js"
        ]
    }
}

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


from django.core.mail import send_mail
from django.conf import settings

# Configuración en settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465  # 587o 465 si usas SSL en lugar de TLS
EMAIL_USE_TLS = False  # Cambia a False si usas SSL
EMAIL_USE_SSL = True  # Cambia a True si usas SSL en lugar de TLS
EMAIL_HOST_USER = 'send@hackerenproceso.com'
EMAIL_HOST_PASSWORD = 'Teamocascas.18321'
DEFAULT_FROM_EMAIL = 'send@hackerenproceso.com'