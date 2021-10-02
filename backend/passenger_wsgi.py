# -*- coding: utf-8 -*-
from django.core.wsgi import get_wsgi_application
import os
import sys
sys.path.insert(0, '/var/www/u1489177/data/www/cok-jest.ru/backend')
sys.path.insert(1, '/var/www/u1489177/data/venv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
application = get_wsgi_application()