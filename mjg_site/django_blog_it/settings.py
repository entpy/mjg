from django.conf import settings
import os

AWS_ENABLED = getattr(settings, 'AWS_ENABLED', False)
BASE_DIR = getattr(settings, 'BASE_DIR')
MEDIA_URL = settings.MEDIA_URL if settings.MEDIA_URL else '/media/'  # settings.MEDIA_URL if settings.MEDIA_URL else '/media/'
MEDIA_ROOT = settings.MEDIA_ROOT if settings.MEDIA_ROOT else os.path.join(BASE_DIR + '/media/')  # settings.MEDIA_ROOT if settings.MEDIA_ROOT else os.path.join(BASE_DIR + '/media/')

DISQUS_SHORTNAME = getattr(settings, 'DISQUS_SHORTNAME', False)

BLOG_TITLE = "MotorJab Garage Blog"
BLOG_DESCRIPTION = "Il blog ufficiale di MotorJab Garage"
BLOG_KEYWORDS = "officina autoriparazioni, meccanica, elettrauto, gommista, ricarica clima"
BLOG_AUTHOR = "motorjab"
SITE_URL = settings.SITE_URL
