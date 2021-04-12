INSTALLED_APPS = (
    "django_pendulum_field",
    "test_app",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.db",
    }
}

USE_TZ = True
TIME_ZONE = "Asia/Seoul"

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

SECRET_KEY = "dummysecret"
