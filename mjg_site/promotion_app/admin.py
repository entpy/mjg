# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class CampaignImageAdmin(admin.ModelAdmin):
    list_display = ('campaign_image_id', 'image', 'size', 'creation_date', )

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'camp_title', 'camp_description', 'msg_subject', 'msg_text', 'was_price', 'final_price', 'small_image', 'large_image', 'campaign_type', 'channel', 'status', 'expiring_date', 'creation_date', 'update_date', )

class CampaignDestAdmin(admin.ModelAdmin):
    list_display = ('campaign_dest_id', 'campaign', 'user', 'code', 'dest', 'channel', 'creation_date', 'update_date', )

class CampaignUserTempAdmin(admin.ModelAdmin):
    list_display = ('campaign_user_temp_id', 'campaign', 'user', 'dest', 'channel', )

class CampaignOrderAdmin(admin.ModelAdmin):
    list_display = ('campaign_order_id', 'campaign', 'user', 'dest', 'code', 'status', 'creation_date', 'update_date', )

admin.site.register(CampaignImage, CampaignImageAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignDest, CampaignDestAdmin)
admin.site.register(CampaignUserTemp, CampaignUserTempAdmin)
admin.site.register(CampaignOrder, CampaignOrderAdmin)
