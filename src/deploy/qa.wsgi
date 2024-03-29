# pinax.wsgi is configured to live in projects/mtn-ism/deploy.

import os
import sys

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "yoza.settings"

sys.path.insert(0, join(settings.PINAX_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
