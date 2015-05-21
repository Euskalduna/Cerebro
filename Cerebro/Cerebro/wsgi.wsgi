"""
WSGI config for Cerebro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cerebro.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""



import os, sys
sys.path.append('/home/evida/Django-Projects/Cerebro')
sys.path.append('/home/evida/Django-Projects/Cerebro/Cerebro')
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkedstats.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'Cerebro.settings'
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

