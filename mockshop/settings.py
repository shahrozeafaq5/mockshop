# settings.py
from pathlib import Path
import os
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------
SECRET_KEY = config('SECRET_KEY', default='change-me')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    "mockshop-1.onrender.com",
    "localhost", "127.0.0.1",
] + [h for h in config('ALLOWED_HOSTS', default='').split(',') if h]

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(default=config("DATABASE_URL"))
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# Apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'csp',             
    'shop',
]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mockshop.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mockshop.wsgi.application'

# -----------------------------------------------------------------------------
# Static / Media
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# -----------------------------------------------------------------------------
# Security & Hardening (addresses ZAP findings)
# -----------------------------------------------------------------------------

# Tell Django requests are HTTPS when behind Render/Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Force HTTPS
SECURE_SSL_REDIRECT = not DEBUG

# HSTS (Strict-Transport-Security)
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'                # clickjacking protection
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://mockshop-1.onrender.com",
]

# -----------------------------------------------------------------------------
# Content Security Policy (CSP) via django-csp
# Adjust sources to exactly what you use.
# -----------------------------------------------------------------------------
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdn.tailwindcss.com",
    "https://unpkg.com",
    "https://cdn.jsdelivr.net",
    "https://fonts.googleapis.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "https://fonts.googleapis.com",
    "'unsafe-inline'",  # remove this if you move all inline styles into CSS files
)
CSP_IMG_SRC = ("'self'", "data:", "https://images.unsplash.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)

# Allow inline scripts only when tagged with a nonce
CSP_INCLUDE_NONCE_IN = ('script-src',)
