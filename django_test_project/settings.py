"""
Minimal Django settings, just enough to get unit tests to run.
"""

from uuid import uuid4

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

DEBUG = True
INSTALLED_APPS = ["django_test_project.app"]
SECRET_KEY = uuid4().hex
