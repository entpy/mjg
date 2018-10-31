# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mjg_site.consts import project_constants
from mjg_site.exceptions import *
import datetime, sys, logging

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
    mobile_number = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(null=True, default=1)
    notify_bitmask = models.IntegerField(default=(project_constants.RECEIVE_MKAUTO_BITMASK + project_constants.RECEIVE_PROMOTIONS_BITMASK + project_constants.RECEIVE_NEWSLETTERS_BITMASK), null=True)
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

        """
        first_name = account_data["first_name"]
        last_name = account_data["last_name"]
        email = account_data["email"]
        mobile_number = account_data["mobile_number"]
        birthday_day = account_data["birthday_day"]
        birthday_month = account_data["birthday_month"]
        birthday_year = account_data["birthday_year"]
        """

        # TODO
        # fare un get_by_email
        # se presente restituire un errore, altrimenti procedere con l'inserimento
        if self.check_if_user_exists(account_data["email"], account_data["mobile_number"]):
            raise UserAlreadyExistsError

        # TODO
        # creo l'oggetto Account che estende l'oggetto User con una relazione 1-1
        new_account_obj = Account(
            user=User.objects.create_user(username=account_data["email"], first_name=account_data["first_name"], last_name=account_data.get("last_name"), email=account_data["email"]),
            mobile_number=account_data.get("mobile_number"),
            birthday_date=self.create_date(date_dictionary=account_data, get_isoformat=True),
        )
        new_account_obj.save(force_insert=True)

        return new_account_obj.user

    def check_if_email_exists(self, email_to_check):
        """Function to check if an email already exists"""
        return_var = None
        try:
            User.objects.get(email=email_to_check)
            return_var = True
        except User.DoesNotExist:
            return_var = False

        return return_var

    def check_mobile_number_exists(self, number_to_check):
        """Function to check if a mobile number already exists"""
        return_var = None
        try:
            User.objects.get(account__mobile_number=number_to_check)
            return_var = True
        except User.DoesNotExist:
            return_var = False

        return return_var

    def check_if_user_exists(self, email, mobile_number=None):
        """Function to check if a user already exists"""
        return_var = False

        # controllo prima se esiste la mail
        if self.check_if_email_exists(email):
            return_var = True

        # controllo se esiste il numero di telefono
        if not return_var and mobile_number:
            if self.check_mobile_number_exists(mobile_number):
                return_var = True

        return return_var

    def create_date(self, date_dictionary=None, get_isoformat=False):
        """Function to create birthday date starting from dd, mm, yyyy"""
        return_var = None

        if date_dictionary:
            day = date_dictionary.get("birthday_day")
            month = date_dictionary.get("birthday_month")
            year = date_dictionary.get("birthday_year")

            # building birthday date
            if (day and month and year):
                if get_isoformat:
                    return_var = date(year=int(year), month=int(month), day=int(day)).isoformat()
                else:
                    return_var = date(year=int(year), month=int(month), day=int(day))

        return return_var

    # TODO
    # controllare le bitmask
    def get_mkauto_accounts(self, days_from_creation):
        """Function to retrieve users list created 'days_from_creation' ago"""
        return_var = None

        return_var = User.objects.values('id', 'first_name', 'last_name', 'email', 'account__mobile_number', 'account__notify_bitmask').filter(account__creation_date__lt=timezone.now()-datetime.timedelta(days=days_from_creation))

	# performing query
        return_var = list(return_var)

        logger.info("elenco utenti: " + str(return_var))

        return return_var

    def get_user_data_as_dictionary(self, user_id):
        """Function to retrieve a user data as dictionary"""
        return_var = None

        try:
            return_var = User.objects.values().get(pk=user_id)
        except User.DoesNotExist:
            # TODO
            # la riga non esiste, mando una mail al developer
            pass

        return return_var
