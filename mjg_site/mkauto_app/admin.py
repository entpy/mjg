# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class MaEventAdmin(admin.ModelAdmin):
    list_display = ('ma_event_id', 'description', 'ma_code', 'prize_type', 'prize_value', 'extra_prize_value', 'start_delay', 'repeat_delay', 'extra_text', 'channels_bitmask', 'ma_event_type', 'json_params', 'status')

class MaEventLogAdmin(admin.ModelAdmin):
    list_display = ('ma_event_log_id', 'user', 'ma_event', 'ma_code', 'creation_date')

class MaEventCodeAdmin(admin.ModelAdmin):
    list_display = ('ma_event_code_id', 'user', 'ma_event', 'ma_event_log', 'code', 'status', 'creation_date', 'update_date')

class MaRandomCodeAdmin(admin.ModelAdmin):
    list_display = ('ma_random_code_id', 'random_code_type', 'random_code', 'order')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'user', 'quality_level', 'feedback_text', 'creation_date')

class MasterAccountCodeAdmin(admin.ModelAdmin):
    list_display = ('master_account_code_id', 'user', 'code', 'creation_date')

class FriendCodeAdmin(admin.ModelAdmin):
    list_display = ('friend_code_id', 'master_account_code', 'ma_event_code', 'status', 'creation_date')

admin.site.register(MaEvent, MaEventAdmin)
admin.site.register(MaEventLog, MaEventLogAdmin)
admin.site.register(MaEventCode, MaEventCodeAdmin)
admin.site.register(MaRandomCode, MaRandomCodeAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(MasterAccountCode, MasterAccountCodeAdmin)
admin.site.register(FriendCode, FriendCodeAdmin)
