# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Account

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# XXX
# Come integrare il modello Account nell'admin
# https://simpleisbetterthancomplex.com/tutorial/2016/11/23/how-to-add-user-profile-to-django-admin.html

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id_account', 'user', 'mobile_number', 'notify_bitmask', 'birthday_date', 'creation_date', 'update_date', 'get_birthday_date_event_done', 'get_feedback_event_done', 'get_review_event_done', 'account_code', 'status')
    readonly_fields = ('update_date', )

admin.site.register(Account, AccountAdmin)
