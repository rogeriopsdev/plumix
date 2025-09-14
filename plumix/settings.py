"""
Django settings for plumix project — pronto para Railway (PostgreSQL + WhiteNoise)
"""

from pathlib import Path
import os
import dj_database_url

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

# --- Ambiente / Segurança ---
DEBUG = os.getenv("DEBUG", "0") == "1"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")  # defina no painel da Railway!
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")  # use "*" ou seu(s) domínio(s)

# Confiança para CSRF no domínio da Railway (adicione seu domínio próprio se tiver)
CSRF_TRUSTED_ORIGINS = [
    "https://plumix-production.up.railway.app",
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

    # UI/Forms
    "crispy_forms",
    "crispy_bootstrap5",
    "widget_tweaks",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static em produção
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

# --- Banco de Dados (Railway usa DATABASE_URL) ---
# Ex.: postgresql://USER:PASS@HOST:PORT/DB?sslmode=require
db_env = "postgresql://postgres:TWzzgXwmSrdErPXOHCKshwiLwHiIGLrJ@postgres.railway.internal:5432/railway"
db_url = os.getenv(db_env, "")

DATABASES = {
    "default": dj_database_url.config(
        env=db_env,   # <- lê a URL do banco da variável DATABASE_URL
        # Fallback local (para DEV) se não houver DATABASE_URL:
        default=(
            f"postgresql://{os.getenv('PGUSER', 'postgres')}:"
            f"{os.getenv('PGPASSWORD', 'ellla81271657')}@{os.getenv('PGHOST', '127.0.0.1')}:"
            f"{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE', 'plumix')}"
        ),
        conn_max_age=600,
        # Em produção: exige SSL EXCETO quando for host interno da Railway
        ssl_require=(
            (os.getenv("DEBUG", "0") != "1") and ("railway.internal" not in db_url)
        ),
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
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Segurança por trás de proxy ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# (opcional) HSTS quando estiver estável em HTTPS:
# SECURE_HSTS_SECONDS = 2592000  # 30 dias
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# --- Auth redirects ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "login"

# --- PK padrão ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
