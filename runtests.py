#!/usr/bin/env python
import sys
import django

from django.conf import global_settings, settings


settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'friendship',
        'friendship.tests',
    ],
    ROOT_URLCONF='friendship.urls',
    MIDDLEWARE_CLASSES=global_settings.MIDDLEWARE_CLASSES + (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',)
)


def runtests(*test_args):
    import django.test.utils

    if django.VERSION[0:2] >= (1, 7):
        django.setup()

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['friendship'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
