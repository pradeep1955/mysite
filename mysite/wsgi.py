"""WSGI config for mysite project."""

import os

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

project_folder = "/home/prdp1955/django_projects/mysite"
load_dotenv(os.path.join(project_folder, ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
