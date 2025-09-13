from pathlib import Path
import os
import dj_database_url

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Segurança
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'chave-secreta-para-dev-apenas')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'plumix-production.up.railway.app',
    'localhost',
    '127.0.0.1'
]
CSRF_TRUSTED_ORIGINS = [
    'https://plumix-production.up.railway.app',
    #'https://avadoc-syk9mjrh.b4a.run'
]

# Cookies de segurança
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plumixapp',
    'usuarios',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plumixapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'plumix.wsgi.application'

# Banco de dados - Railway (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
       default='postgresql://postgres:KHisXMTxzORwdvvIBfhMZDjATbqmzKEC@switchback.proxy.rlwy.net:33693/railway',
        conn_max_age=600,
       ssl_require=True
    )
}
#DATABASES = {
 #  'default': {
  #    'ENGINE': 'django.db.backends.sqlite3',
   #  'NAME': BASE_DIR / 'dbi.sqlite3',
#}
#}

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = []

# --- Segurança em produção por trás de proxy ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# (opcional) HSTS — ative quando estiver 100% em HTTPS estável
# SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# --- Auth redirects ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "login"

# --- Chave padrão de PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
