"""
WSGI config for simple_todo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append("/home/cybermals.heliohost.us/httpdocs/simple-todo/simple_todo/")
sys.path.append("/home/cybermals.heliohost.us/httpdocs/simple-todo/simple_todo/simple_todo/")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_todo.settings')

application = get_wsgi_application()
app = application
