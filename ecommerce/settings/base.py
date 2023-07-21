import os

SECRET_KEY = "django-insecure-2y!qbi4g^x88l_fdvmh%g3(i-o3^+7#k=ps@v_1%+l@m9bktwh"

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


INSTALLED_APPS = [
    # "store.apps.StoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_reorder",
    "django.contrib.sites",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware" ,
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]


ADMIN_REORDER = (
    # Keep original label and models
    #'store',
    # Reorder app models
    {
        "app": "store",
        "models": (
            "store.Customer",
            "store.Order",
            "store.Product",
            "store.OrderItem",
            "store.ShippingAddress",
            "store.CustomerOrderHistory",
            "store.ProxyCustomer",
        ),
    },
    # Rename app
    {"app": "auth", "label": "Authorize"},
    # Exclude models
    # {'app': 'auth', 'models': ('auth.User', )},
    # # Cross-linked models
    # {'app': 'auth', 'models': ('auth.User', 'sites.Site')},
    # models with custom name
    # {'app': 'auth', 'models': (
    #     'auth.Group',
    #     {'model': 'auth.User', 'label': 'Staff'},
    # )},
)
ROOT_URLCONF = "ecommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates", "store"), BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = "Asia/Karachi"


USE_I18N = True

USE_L10N = True

USE_TZ = True


WSGI_APPLICATION = "ecommerce.wsgi.application"

STATIC_URL = "/static/"


from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = "en"

LANGUAGES = (
    ('en',_('English')),
    ('fr',_('French')),
)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/images/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/images")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
