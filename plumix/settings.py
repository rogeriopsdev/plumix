"""
Django settings for plumix project (pronto para Railway).

- Banco: PostgreSQL via DATABASE_URL (Railway/Postgres plugin)
- Static: WhiteNoise (serve /static em produção)
- Segurança: HTTPS via proxy + CSRF confiando em *.railway.app
"""

from pathlib import Path
import os
import dj_database_url

# --- Diretórios base ---
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

# --- Básico / Ambiente ---
DEBUG = os.getenv("DEBUG", "0") == "1"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")  # defina no Railway!
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")  # use "*" na Railway ou seu domínio

# Confie no domínio da Railway (adicione seu domínio custom se tiver)
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    # "https://seu-dominio.com",
]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # seus apps
    "plumixapp",
    "usuarioapp",

    # UI helpers
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # <— habilita servir static em produção
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "plumix.urls"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "plumix.wsgi.application"

# --- Banco de Dados (PostgreSQL via DATABASE_URL) ---
# Railway injeta DATABASE_URL quando você adiciona o plugin Postgres.
# Ex.: postgresql://usuario:senha@host:5432/dbname
DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        # fallback local (se DATABASE_URL não existir):
        default=(
            f"postgresql://{os.getenv('PGUSER', 'postgres')}:"
            f"{os.getenv('PGPASSWORD', '')}@{os.getenv('PGHOST', '127.0.0.1')}:"
            f"{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE', 'plumix')}"
        ),
        conn_max_age=600,           # pooling
        ssl_require=not DEBUG,      # SSL em produção
    )
}

# --- Localização / Tempo ---
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Araguaina"
USE_I18N = True
USE_TZ = True

# --- Static (WhiteNoise) ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# opcional: diretório de estáticos do projeto (além dos dos apps)
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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
