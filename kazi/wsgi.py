"""
WSGI config for kazi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/noone/projects/kazi-web/kazi'
if path not in sys.path:
    sys.path.append(path)


activate_this = '/home/noone/projects/kazi-web/env/bin/activate_this.py'
exec(compile(open(activate_this,"rb").read(),activate_this, 'exec'), dict(__file__=activate_this))



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kazi.settings")



application = get_wsgi_application()
