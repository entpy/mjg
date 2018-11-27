# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Func, F, Q

# from django.db.models.signals import post_save
from django.dispatch import receiver
from mjg_site.consts import project_constants
from mjg_site.exceptions import *
import datetime, sys, logging, base64, hashlib

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
    notify_bitmask = models.IntegerField(default=(project_constants.RECEIVE_MKAUTO_BITMASK + project_constants.RECEIVE_PROMOTIONS_BITMASK + project_constants.RECEIVE_NEWSLETTERS_BITMASK), null=True)
    birthday_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    get_birthday_date_event_done = models.IntegerField(null=True, blank=True, default=0)
    get_feedback_event_done = models.IntegerField(null=True, blank=True, default=0)
    get_review_event_done = models.IntegerField(null=True, blank=True, default=0)
    account_code = models.CharField(max_length=20, null=False, blank=False)
    status = models.IntegerField(null=True, default=1)

    class Meta:
        app_label = 'account_app'
        indexes = [
            models.Index(fields=['get_feedback_event_done',]),
            models.Index(fields=['get_review_event_done',]),
            models.Index(fields=['birthday_date',]),
            models.Index(fields=['creation_date',]),
            models.Index(fields=['notify_bitmask',]),
            models.Index(fields=['account_code',]),
            models.Index(fields=['status',]),
        ]

    def __unicode__(self):
        return self.user.email

    """
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)
        instance.account.save()
    """

    def save(self, *args, **kwargs):
        # setto il campo account_code
        if not self.account_code:
            self.account_code = self.__generate_account_code(email=self.user.email)
        super(Account, self).save(*args, **kwargs) # Call the "real" save() method.

    def update_account(self, save_data, user_obj):
        """Function to update User and Account data"""
        return_var = False

        # se ho passato la mail e il telefono e sono diversi da quelli già
        # presenti, controllo che non siano già utilizzati
        if (save_data.get("email") and save_data.get("email") != user_obj.email):
            if self.check_if_email_exists(email_to_check=save_data.get("email")):
                # email modificata ma già presente
                raise UserAlreadyExistsError

        if (save_data.get("mobile_number") and save_data.get("mobile_number") != user_obj.account.mobile_number):
            if self.check_mobile_number_exists(number_to_check=save_data.get("mobile_number")):
                # telefono modificato ma già presente
                raise UserAlreadyExistsError

        if save_data and user_obj:
            # save User model addictional informations
            if "first_name" in save_data:
                user_obj.first_name = save_data["first_name"]
            if "last_name" in save_data:
                user_obj.last_name = save_data["last_name"]
            if "email" in save_data:
                user_obj.email = save_data["email"]
            # save Account model addictional informations
            if "status" in save_data:
                user_obj.account.status = save_data["status"]
            # if "birthday_date" in save_data:
            #    user_obj.account.birthday_date = save_data["birthday_date"]
            if "mobile_number" in save_data:
                user_obj.account.mobile_number = save_data["mobile_number"]
            if "notify_bitmask" in save_data:
                user_obj.account.notify_bitmask = save_data["notify_bitmask"]
            if "get_birthday_date_event_done" in save_data:
                user_obj.account.get_birthday_date_event_done = save_data["get_birthday_date_event_done"]
            if "get_feedback_event_done" in save_data:
                user_obj.account.get_feedback_event_done = save_data["get_feedback_event_done"]
            if "get_review_event_done" in save_data:
                user_obj.account.get_review_event_done = save_data["get_review_event_done"]

            # se presente gg mm aaaa salvo anche la data di nascita
            birthday_date = self.create_date(date_dictionary=save_data, get_isoformat=True)
            if "birthday_day" in save_data and "birthday_month" in save_data and "birthday_year" in save_data:
                user_obj.account.birthday_date = birthday_date

            # save addictiona models data
            user_obj.save()
            user_obj.account.save()
            return_var = user_obj

        if not return_var:
            logger.errro("Errore in update_account nel salvataggio dei dati: " + str(save_data))
            raise UpdateUserDataError

        return return_var

    def __generate_account_code(self, email):
        """
        Function to convert email to username
        taken from -> https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
        """
        # Emails should be case-insensitive unique
        email = email.lower()
        # Deal with internationalized email addresses
        converted = email.encode('utf8', 'ignore')

        return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:20]

    # bitwise functions {{{
    def check_bitmask(self, b1, b2):
        """Function to compare two bitmask 'b1' and 'b2'"""
        return int(b1) & int(b2)

    def add_bitmask(self, bitmask, add_value):
        """Function to add bitmask 'add_value' to 'bitmask'"""
        return int(bitmask) | int(add_value);

    def remove_bitmask(self, bitmask, remove_value):
        """Function to remove bitmask 'remove_value' from 'bitmask'"""
        return int(bitmask) & (~int(remove_value));
    # bitwise functions }}}

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

        # fare un get_by_email
        # se presente restituire un errore, altrimenti procedere con l'inserimento
        if self.check_if_user_exists(account_data["email"], account_data["mobile_number"]):
            raise UserAlreadyExistsError

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
                    return_var = datetime.date(year=int(year), month=int(month), day=int(day)).isoformat()
                else:
                    return_var = datetime.date(year=int(year), month=int(month), day=int(day))

        return return_var

    # TODO
    # controllare le bitmask
    def get_mkauto_accounts(self, days_from_creation, event_code=None):
        """Function to retrieve users list created 'days_from_creation' ago"""
        # -------NOW-80---CREAZIONE(NOW-40)---NOW-20----NOW-------
        # ----------|--------------|-------------|-------|--------
        return_var = None

        # solo gli utenti registrati da almeno x giorni
        return_var = User.objects.values('id', 'first_name', 'last_name', 'email', 'account__mobile_number', 'account__notify_bitmask').filter(account__creation_date__date__lte=(timezone.now()-datetime.timedelta(days=days_from_creation)).date())
        # solo gli utenti che vogliono ricevere queste notifiche (controllo la bitmask)
        return_var = return_var.annotate(bitmask_annotated_field=F('account__notify_bitmask').bitand(project_constants.RECEIVE_MKAUTO_BITMASK))
        return_var = return_var.filter(bitmask_annotated_field__gt=0)
        # solo gli utenti attivi (status=1)
        return_var = return_var.filter(account__status=1)
        return_var = return_var.filter(is_staff=False)
        # return_var = return_var.filter(account__notify_bitmask__gte=F('account__notify_bitmask').bitand(project_constants.RECEIVE_MKAUTO_BITMASK))

        logger.info("get account with code: " + str(event_code))

        # filtri dedicati agli eventi
        if event_code == "get_birthday_date":
            # solo se l'utente non ha la data di nascita
            return_var = return_var.filter(account__birthday_date__isnull=True, account__get_birthday_date_event_done=0)

        if event_code == "happy_birthday_prize":
            # solo se il compleanno dell'utente è oggi
            return_var = return_var.filter(account__birthday_date__month=timezone.now().month, account__birthday_date__day=timezone.now().day)

        if event_code == "get_feedback":
            # solo se l'utente non ha ancora lasciato feedback (info interne)
            return_var = return_var.filter(account__get_feedback_event_done=0)

        if event_code == "get_review":
            # solo se l'utente non ha ancora lasciato recensioni (info pubbliche)
            return_var = return_var.filter(account__get_review_event_done=0)

	# performing query
        return_var = list(return_var)

        # dat = (timezone.now()-datetime.timedelta(days=days_from_creation)).date()
        # logger.info("date: " + str(dat))
        logger.info("elenco utenti: " + str(return_var))

        return return_var

    def get_user_data_as_dictionary(self, user_id):
        """Function to retrieve a user data as dictionary"""
        return_var = None

        try:
            return_var = User.objects.values('id', 'first_name', 'last_name', 'email', 'account__account_code').get(pk=user_id)
        except User.DoesNotExist:
            # TODO
            # la riga non esiste, mando una mail al developer
            pass

        return return_var

    def get_user_by_id_account_code(self, user_id, account_code):
        """Function to retrieve an User instance by user_id and account_code"""
        return_var = None

        try:
            return_var = User.objects.get(pk=user_id, account__account_code=account_code)
        except User.DoesNotExist:
            # XXX
            # la riga non esiste, mando una mail al developer
            pass

        return return_var

    def get_user_by_id(self, user_id):
        """Function to retrieve an User instance by user_id"""
        return_var = None

        try:
            return_var = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # XXX
            # la riga non esiste, mando una mail al developer
            pass

        return return_var

    def sort_field_wrapper(self, request):
        """Function to map table order with db order"""

        return_var = None

        if request.GET.get("sorts[first_name]"):
            return_var = str("-" if int(request.GET.get("sorts[first_name]")) == -1 else "") + "first_name"
        if request.GET.get("sorts[last_name]"):
            return_var = str("-" if int(request.GET.get("sorts[last_name]")) == -1 else "") + "last_name"
        if request.GET.get("sorts[email]"):
            return_var = str("-" if int(request.GET.get("sorts[email]")) == -1 else "") + "email"
        if request.GET.get("sorts[account__mobile_number]"):
            return_var = str("-" if int(request.GET.get("sorts[account__mobile_number]")) == -1 else "") + "account__mobile_number"
        if request.GET.get("sorts[account__birthday_date_str]"):
            return_var = str("-" if int(request.GET.get("sorts[account__birthday_date_str]")) == -1 else "") + "account__birthday_date"
        if request.GET.get("sorts[account__creation_date_str]"):
            return_var = str("-" if int(request.GET.get("sorts[account__creation_date_str]")) == -1 else "") + "account__creation_date"

        return return_var

    def get_accounts(self, limit = None, offset = None, sort_field = None, search_text = None):
        """Function to retrieve an active users list"""
        return_var = None

        # solo gli utenti attivi (status=1) e che non siano staff (is_staff=False)
        return_var = User.objects.values('id', 'first_name', 'last_name', 'email', 'account__mobile_number', 'account__notify_bitmask', 'account__creation_date', 'account__birthday_date').filter(account__status=1, is_staff=False)
        return_var = return_var.annotate(account__creation_date_str=Func(F('account__creation_date'), function="DATE"))
        return_var = return_var.annotate(account__birthday_date_str=Func(F('account__birthday_date'), function="DATE"))
        # return_var = return_var.extra(select={'datestr':"to_char(mjg_sandbox_account.creation_date, 'YYYY-MM-DD')"}).values_list('datestr', flat='true')

        # eventuali ordinamenti
        if sort_field:
            return_var = return_var.order_by(sort_field)

        # TODO
        # implementare qui la ricerca
	if search_text:
	    return_var = return_var.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text) | Q(email__icontains=search_text) | Q(account__mobile_number__icontains=search_text))

	# se presenti imposto l'offset e il limite della query
	# Es. -> [5:10]
	# 	 [offset:limit]
	if offset and limit:
            return_var = return_var[limit:offset]
	elif limit:
            return_var = return_var[:limit]

	# performing query
        return_var = list(return_var)

        logger.info("elenco utenti: " + str(return_var))

        return return_var

    def count_total_account(self):
	"""Function to count all active accounts"""
	return_var = 0

	# conteggio solo gli utenti attivi (status=1) e che non siano staff (is_staff=False)
        return_var = User.objects.filter(account__status=1, is_staff=False).count()

	return return_var
