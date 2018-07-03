#!/usr/bin/env python
import sys

import django
from django.conf import global_settings, settings


if django.VERSION[0:2] < (2, 0):
    CURRENT_MIDDLEWARE = global_settings.MIDDLEWARE_CLASSES
else:
    CURRENT_MIDDLEWARE = global_settings.MIDDLEWARE

OUR_MIDDLEWARE = []
OUR_MIDDLEWARE.extend(CURRENT_MIDDLEWARE)
OUR_MIDDLEWARE.extend([
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
])


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
    MIDDLEWARE=OUR_MIDDLEWARE,
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
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
