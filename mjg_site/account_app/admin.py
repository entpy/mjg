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

"""
class ProfileInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Account'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    fieldsets = (
            ('USER', {
                    'fields': (
                            'first_name',
                            'last_name',
                            'email',
                            'password',
                            )
                    }
            ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
"""
admin.site.register(Account)
