import os
import django
from channels.routing import get_default_application
# import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seriessy.settings.production")
django.setup()
channel_layer = get_default_application()
