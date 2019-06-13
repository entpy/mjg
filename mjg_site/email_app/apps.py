# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class EmailAppConfig(AppConfig):
    name = 'email_app'

    def ready(self):
        # https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
        # import mjg_site.email_app.signals  # noqa
        import email_app.signals  # noqa
	pass
