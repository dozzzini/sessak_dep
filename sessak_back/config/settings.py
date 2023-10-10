from pathlib import Path
import os, environ
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")


# Application definition
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    # 소셜로그인 시 필요한 settings
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "django.contrib.sites",
    "social_django",
    "allauth",
    "allauth.account",
    "rest_auth",
    "rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.google",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "posts.apps.PostsConfig",
    "comments.apps.CommentsConfig",
    "categories.apps.CategoriesConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = CUSTOM_APPS + SYSTEM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 추가
    "django.middleware.common.CommonMiddleware",  # CORS 추가
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]
CSRF_TRUSTED_ORIGINS = [
    "https://port-0-sessak-back2-cgw1f2almhig6l2.sel5.cloudtype.app",
]
CORS_ALLOWED_ORIGIN = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://port-0-sessak-back2-cgw1f2almhig6l2.sel5.cloudtype.app",
]
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://port-0-sessak-back2-cgw1f2almhig6l2.sel5.cloudtype.app",
)
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}


GOOGLE_AUTH_CLIENT_ID = get_env_variable("GOOGLE_AUTH_CLIENT_ID")
GOOGLE_AUTH_SECRET = get_env_variable("GOOGLE_AUTH_SECRET")


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILE_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 징고 allauth
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "social_core.backends.kakao.KakaoOAuth2",
    "social_core.backends.google.GoogleOAuth2",  # <-- 구글
)
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"  # 로그인 후 리디렉션할 페이지
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # 로그아웃 후 리디렉션 할 페이지
ACCOUNT_LOGOUT_ON_GET = True  # 로그아웃 버튼 클릭 시 자동 로그아웃

# Auth
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # 배포할 때 지워야 함
    ),
}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_USE_JWT = True
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}


WSGI_APPLICATION = "config.wsgi.application"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# # 배포용
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": get_env_variable("NAME"),
#         "HOST": get_env_variable("HOST"),
#         "USER": get_env_variable("USER"),
#         "PASSWORD": get_env_variable("PASSWORD"),
#         "PORT": get_env_variable("PORT"),
#     }
# }
