import os
import sys
sys.path.append("/home/ubuntu/mosaic-webui/")
sys.path.append("/home/ubuntu/mosaic-webui/mosaic/")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mosaic.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
