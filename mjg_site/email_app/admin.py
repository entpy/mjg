# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class EmailSentAdmin(admin.ModelAdmin):
    list_display = ('email_sent_id', 'user', 'email_code', 'dest', 'email_type', 'type_id', 'status_bitmask', 'creation_date', 'update_date', )

admin.site.register(EmailSent, EmailSentAdmin)
