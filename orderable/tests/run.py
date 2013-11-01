"""From http://stackoverflow.com/a/12260597/400691"""
import sys

from django.conf import settings


settings.configure(
    DATABASES={'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'orderable',
        'HOST': 'localhost'
    }},
    INSTALLED_APPS=(
        'orderable.tests',
    ),
)
try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['orderable'])
if failures:
    sys.exit(1)
