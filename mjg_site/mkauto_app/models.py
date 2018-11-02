# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mjg_site.consts import project_constants
from mjg_site.exceptions import *
from mkauto_app.strings import MkautoStrings
from mkauto_app.consts import mkauto_consts
from account_app.models import Account
from email_app.email_core import CustomEmailTemplate
import datetime, random, string, sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MaEvent(models.Model):
    PRIZE_TYPE = (
        ('discount', '%'),
        ('bonus', '€'),
        ('text', 'Text'),
    )
    ma_event_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name="Una descrizione dell'evento")
    ma_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Codice identificativo dell'evento")
    prize_type = models.CharField(max_length=10, null=False, blank=False, choices=PRIZE_TYPE, verbose_name="Il tipo di premio es. discount, bonus, text")
    prize_value = models.CharField(max_length=200, null=False, blank=False, verbose_name="Il premio es. 30, una pizza, ...")
    start_delay = models.IntegerField(null=True, blank=True, verbose_name="L'evento viene spedito se l'utente è creato da almeno questi giorni")
    repeat_delay = models.IntegerField(null=True, blank=True, verbose_name="Dopo il primo invio, tutti i successivi sono ogni x giorni, indicati da questo numero")
    # send_date = models.DateField(null=True, blank=True, verbose_name="Alternativo a start_date e repeat_date, se settato indica l'invio puntuale dell'evento in una certa data")
    extra_text = models.TextField(null=False, blank=True, verbose_name="Testo aggiuntivo, es. le limitazioni dei coupo per questo evento")
    is_tickle = models.BooleanField(blank=True, verbose_name="Se 1 l'evento è un tickle, se è 0 l'evento è un premio")
    channels_bitmask = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name="Indica su quali canali inviare l'evento, per il momento esiste solo il channel email")
    prize_call_to_action = models.CharField(max_length=200, null=True, blank=True, verbose_name="Se settato il premio avrà una call to action")
    tickle_call_to_action = models.CharField(max_length=200, null=True, blank=True, verbose_name="Se settato il tickle avrà una call to action")
    status = models.NullBooleanField(null=True, blank=True, default=0, verbose_name="Indica se l'evento è attivo o no (1=attivo, 0=non attivo)")

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return self.ma_event_id

    def get_by_ma_code(self, ma_code):
        """Funtion to retrieve ma_event by ma_code"""
        return_var = None

        try:
            return_var = MaEvent.objects.values().get(ma_code=ma_code)
        except MaEvent.DoesNotExist:
            # TODO
            # la riga non esiste, mando una mail al developer
            raise 

        return return_var

    def event_can_be_performed(self, ma_event_id, repeat_delay, user_id):
        """
        Se l'id dell'evento non è presente nella tabella ma_event_log posso inviare l'evento
        Se l'id dell'evento è presente nella tabella ma_event_log devo controllare che i giorni 
        della data dell'ultimo inserimento siano > dei giorni in repeat_delay
        """
        return_var = False

        # return_var = MaEventLog.objects.values('creation_date').filter(user__id=user_id, creation_date__gt=timezone.now()-datetime.timedelta(days=repeat_delay)).last()
        return_var = MaEventLog.objects.values('ma_event_log_id', 'creation_date').filter(user__id=user_id, ma_event__ma_event_id=ma_event_id).order_by('-ma_event_log_id').first()
        # return_var = return_var.order_by('-ma_event_log_id')[:1]
        if not return_var:
            # event_log non ancora esistente, posso inviare l'evento
            return_var = True
        elif return_var.get("creation_date") >= timezone.now()-datetime.timedelta(days=repeat_delay):
            # controllo che i giorni della data dell'ultimo inserimento siano > dei giorni in repeat_delay
            return_var = True

        return return_var

    def add_event_log(self, user_id, ma_event_id, ma_code):
        """
        In base al risultato della funzione event_can_be_performed decido se inserire un ma_event_log, cioè:
        se posso inviare l'evento inserisco un nuovo log
        se non posso inviare l'evento non inserisco un nuovo log ed esco dalla funzione
        """

        ma_event_log_obj = MaEventLog.objects.create(user_id=user_id, ma_event_id=ma_event_id, ma_code=ma_code)

        return ma_event_log_obj

    def add_event_code(self, user_id, ma_event_id, ma_event_log_id, ma_code):
        """Creo una nuova riga con un codice random"""

        coupon_code = self.generate_random_code()
        ma_event_code_obj = MaEventCode.objects.create(user_id=user_id, ma_event_id=ma_event_id, ma_event_log_id=ma_event_log_id, ma_code=ma_code, code=coupon_code)

        return coupon_code

    def create_event_strings(self, ma_code, prize_type, values_dictionary={}, is_tickle=False):
        """
        Function to build event strings disctionary (subject, title and content)
        qui restituisco le label con ancora le variabili da sostitutire, es {{prize_value}}, {{name}}, ...
        i valori verranno sostituiti in un secondo momento.

        Per ottenere una stringa con le variabili sostituite:
        MkautoStrings.get_string(key=MkautoStrings.strings[ma_code + "." + prize_type + ".subject"], values_dictionary=values_dictionary)
        i valori verranno sostituiti con return self.strings[key].format(**values_dictionary) <- vedere oggetto strings.py
        """

        if is_tickle:
            ma_code += "_tickle"
        
        return {
            "subject" : self.create_first_name_string(string=MkautoStrings.get_string(key=ma_code + "." + prize_type + ".subject", values_dictionary=values_dictionary), separator=', ', first_name=values_dictionary.get("first_name")),
            "title" : self.create_first_name_string(string=MkautoStrings.get_string(key=ma_code + "." + prize_type + ".title", values_dictionary=values_dictionary), separator=',<br />', first_name=values_dictionary.get("first_name")),
            "content" : MkautoStrings.get_string(key=ma_code + "." + prize_type + ".content", values_dictionary=values_dictionary),
            "call_to_action_title" : MkautoStrings.get_string(key=ma_code + ".prize_call_to_action.title"),
            "call_to_action_label" : MkautoStrings.get_string(key=ma_code + ".prize_call_to_action.label"),
            "coupon_code_extra_text" : MkautoStrings.get_string(key=ma_code + ".prize_call_to_action.label"),
            "image_code" : ma_code,
        }

    def create_first_name_string(self, string, separator, first_name=""):
        """
        Function to create title or subject string
        es. Subject: Name, welcome to ... or Welcome to ...
        es. Title: Name,<br /> welcome to ... or Welcome to ...
        separator can be: ', ' or ',<br />'
        """
        # create first name string
        return self.ucfirst(first_name + separator + string)

    #TODO
    def make_prize(self, user_id, ma_code=None, ma_code_dictionary=None, is_tickle=False):
        """
        Function to send a prize
            - ma_code lo utilizzo solo se non ho già tutti i dati in ma_code_dictionary per fare una get by code,
              fatta la get_by_code inserisco i dati nel dizionario ma_code_dictionary
            - is_tickle lo setto a True se l'evento deve essere di tipo _tickle, quindi non genero un codice ma inserisco una call to action nel codice

            1) Controllo se posso inviare l'evento. in base allo start/repeat delay e la tabella ma_event_log
            2) Inserisco una riga in ma_event_log
            3) Creo una riga in ma_event_code
            4) Genero i testi per la mail (oggetto, titolo e testo) in base al tipo di premio e all'evento
            5) Sostituisco ai testi le variabili
            5) Invio il premio (il codice generato in ma_event_code) all'utente via email
        """

        if not ma_code_dictionary:
            # TODO
            # faccio una get_by_ma_code e riempo il dizionario ma_code_dictionary
            ma_code_dictionary = self.get_by_ma_code(ma_code=ma_code)

        if not ma_code_dictionary:
            # problemi con il codice passato alla funzione
            raise MaEventsCodeDoesNotExistError

        logger.info("MaEvent info dict")
        logger.info(ma_code_dictionary)

        # 1)
        # Controllo se l'evento può essere inviato
        if not self.event_can_be_performed(ma_event_id=ma_code_dictionary["ma_event_id"], repeat_delay=ma_code_dictionary["repeat_delay"], user_id=user_id):
            # l'evento non può essere inviato (perchè non ancora oltre il repeat_delay)
            return False

        # 2)
        # L'evento può essere inviato, inserisco una riga in ma_event_log
        ma_event_log_obj = self.add_event_log(user_id=user_id, ma_event_id=ma_code_dictionary["ma_event_id"], ma_code=ma_code_dictionary["ma_code"])

        # prelevo le info dell'account
        account_obj = Account()
        account_info_dictionary = account_obj.get_user_data_as_dictionary(user_id=user_id)

        # 3)
        # Creo una riga in ma_event_code (ma solo se l'evento non è di tipo tickle)
        coupon_code = False
        if not is_tickle:
            coupon_code = self.add_event_code(user_id=user_id, ma_event_id=ma_code_dictionary["ma_event_id"], ma_event_log_id=ma_event_log_obj.ma_event_log_id, ma_code=ma_code_dictionary["ma_code"])

        # 4)
        # Genero i testi per la mail (oggetto, titolo e testo) in base al tipo di premio e all'evento
        # creo il dizionario con le chiavi e i valori da sostituire nella mail, all'interno
        # della funzione "create_event_strings" se l'evento è "tickle" appendo al codice "_tickle"
        values_dictionary = {
            "first_name" : account_info_dictionary["first_name"],
            "prize_val" : ma_code_dictionary["prize_value"],
            "coupon_limitations" : ma_code_dictionary["extra_text"],
        }

        event_strings = self.create_event_strings(
            ma_code=ma_code_dictionary["ma_code"],
            prize_type=ma_code_dictionary["prize_type"],
            values_dictionary=values_dictionary,
            is_tickle=is_tickle
        )

        # 6) Creo la mail con i testi definitivi e invio la mail
        email_context = {
            "subject" : event_strings["subject"],
            "title" : event_strings["title"],
            "content" : event_strings["content"],
            "image_code" : event_strings["image_code"],
            "coupon_code" : coupon_code,
            "coupon_code_extra_text" : event_strings["coupon_code_extra_text"],
        }
        CustomEmailTemplate(email_name="mkauto_email", email_context=email_context, recipient_list=[account_info_dictionary["email"],])

        logger.info("@@@ Stringhe finali @@@")
        logger.info(event_strings)

        return True

    #TODO
    def make_tickle(self):
        """Function to send a tickle"""

    def generate_random_code(self, depth = 0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        try:
            # checking if code already exists
            MaEventCode.objects.get(code=random_code)

            # than recall this function to generate a new ones
            if depth < 50:
                random_code = self.generate_random_code(self, depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        except MaEventCode.DoesNotExist:
            # il codice non esiste in db pertano può essere utilizzato
            pass

        return random_code

    def create_mkauto_defaults(self):
        """Function to create defaults about mkauto events"""

        # svuoto la tabella con i default
        MaEvent.objects.all().delete()

        if mkauto_consts:
            for mkauto_row in mkauto_consts.mkauto_default_values:
                ma_event_obj = MaEvent()
                ma_event_obj.ma_code = mkauto_row.get("ma_code")
                ma_event_obj.description = mkauto_row.get("description")
                ma_event_obj.prize_type = mkauto_row.get("prize_type")
                ma_event_obj.prize_value = mkauto_row.get("prize_value")
                ma_event_obj.start_delay = mkauto_row.get("start_delay")
                ma_event_obj.repeat_delay = mkauto_row.get("repeat_delay")
                ma_event_obj.extra_text = mkauto_row.get("extra_text")
                ma_event_obj.is_tickle = mkauto_row.get("is_tickle")
                ma_event_obj.prize_call_to_action = mkauto_row.get("prize_call_to_action")
                ma_event_obj.tickle_call_to_action = mkauto_row.get("tickle_call_to_action")
                ma_event_obj.status = mkauto_row.get("status")
                ma_event_obj.save(force_insert=True)

        return True

    def ucfirst(self, string):
        """Function to capitalize first letter about a string"""
        return_var = None
        if string:
            return_var = string[0].upper() + string[1:]

        return return_var

    # TODO
    def ma_cleaning(self):
        """
        Function to delete old ma_event_log and ma_event_code
        Basta eliminare solo le righe più vecchie di un anno dalla tabella ma_event_log,
        in quanto verranno eliminati automaticamente anche gli ma_event_code,
        tramite l'utilizzo di on_delete=models.CASCADE
        """

        return True

    # TODO
    def get_active_ma_events(self):
        """Function to retrieve a dictionary of all active events"""
        return_var = {}

        active_events = MaEvent.objects.values().filter(status=1)
        if active_events:
            for val in active_events:
                return_var[val["ma_code"]] = val
        return return_var

class MaEventLog(models.Model):
    ma_event_log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_maeventlog', on_delete=models.CASCADE)
    ma_event = models.ForeignKey(MaEvent, null=True, on_delete=models.SET_NULL)
    ma_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Codice identificativo dell'evento")
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return self.ma_event_log_id

class MaEventCode(models.Model):
    ma_event_code_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_maeventcode', on_delete=models.CASCADE)
    ma_event = models.ForeignKey(MaEvent, null=True, on_delete=models.SET_NULL)
    ma_event_log = models.ForeignKey(MaEventLog, on_delete=models.CASCADE)
    ma_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Codice identificativo dell'evento")
    code = models.CharField(max_length=15, null=False, blank=False)
    status = models.IntegerField(null=False, blank=False, default=1, verbose_name="Indica se il codice è utilizzato o no (1=non utilizzato 2=utilizzato)")
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return self.ma_event_code_id
