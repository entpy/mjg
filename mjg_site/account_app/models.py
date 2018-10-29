# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from mjg_site.consts import project_constants
import sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

# extends User model
class Account(models.Model):
    # first_name, last_name, email sono nel modello di default User
    id_account = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) # Links Account to a User model instance.
    mobile_number = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, default=1)
    notify_bitmask = models.CharField(max_length=20, default=(project_constants.RECEIVE_MKAUTO_BITMASK + project_constants.RECEIVE_PROMOTIONS_BITMASK + project_constants.RECEIVE_NEWSLETTERS_BITMASK), null=True)
    birthday_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'account_app'

    def __unicode__(self):
        return self.user.email

    # TODO
    def create_account(self, account_data):
        """Function to create a new account"""

        logger.info("account data: " + str(account_data))

        first_name = account_data["first_name"]
        last_name = account_data["last_name"]
        email = account_data["email"]
        mobile_number = account_data["mobile_number"]
        birthday_day = account_data["birthday_day"]
        birthday_month = account_data["birthday_month"]
        birthday_year = account_data["birthday_year"]

        # TODO
        # fare un get_by_email
        # se presente restituire un errore, altrimenti procedere con l'inserimento

        return True
