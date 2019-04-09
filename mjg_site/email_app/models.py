# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mjg_site.consts import project_constants
import datetime, sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class EmailSent(models.Model):
    CAMPAIGN_TYPE = (
        (project_constants.CAMPAIGN_TYPE_PROMOTION, project_constants.CAMPAIGN_TYPE_PROMOTION),
        (project_constants.CAMPAIGN_TYPE_NEWSLETTER, project_constants.CAMPAIGN_TYPE_NEWSLETTER),
        (project_constants.CAMPAIGN_TYPE_MKAUTO, project_constants.CAMPAIGN_TYPE_MKAUTO),
    )
    email_sent_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_code = models.CharField(max_length=200, null=False, blank=False, verbose_name="Il codice fornito dal provider")
    dest = models.CharField(max_length=50, null=False, blank=False, verbose_name="L'indirizzo email di destinazione")
    email_type = models.CharField(max_length=30, null=False, blank=False, choices=CAMPAIGN_TYPE, verbose_name="Tipo di email (mkauto,promozione,newsletter)")
    type_id = models.IntegerField(null=False, blank=False, verbose_name="L'id della promozione/newsletter o l'id dell'evento della mkauto")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'email_app'
        indexes = [
            models.Index(fields=['email_code',]),
            models.Index(fields=['dest',]),
            models.Index(fields=['email_type',]),
            models.Index(fields=['type_id',]),
        ]

    def __unicode__(self):
        return str(self.email_sent_id)

    # TODO
    def set_email_sent(self, email_type, type_id, user_id, dest, email_code):
        """Function to add a new email sent"""

        email_sent_obj = EmailSent()
        email_sent_obj.email_type = email_type
        email_sent_obj.type_id = type_id
        email_sent_obj.user_id = user_id
        email_sent_obj.dest = dest
        email_sent_obj.email_code = email_code
        email_sent_obj.save()

        return email_sent_obj.email_sent_id
