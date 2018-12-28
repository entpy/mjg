# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.conf import settings
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
    MA_EVENT_TYPE = (
        (mkauto_consts.ma_event_type["prize"], mkauto_consts.ma_event_type["prize"]),
        (mkauto_consts.ma_event_type["prize_tickle"], mkauto_consts.ma_event_type["prize_tickle"]),
        # (mkauto_consts.ma_event_type["scheduled"], mkauto_consts.ma_event_type["scheduled"]),
        (mkauto_consts.ma_event_type["tip"], mkauto_consts.ma_event_type["tip"]),
        (mkauto_consts.ma_event_type["monthly_prize"], mkauto_consts.ma_event_type["monthly_prize"]),
    )
    ma_event_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name="Una descrizione dell'evento")
    ma_code = models.CharField(max_length=50, null=False, blank=False, unique=True, verbose_name="Codice identificativo dell'evento")
    prize_type = models.CharField(max_length=10, null=True, blank=True, choices=PRIZE_TYPE, verbose_name="Il tipo di premio es. discount, bonus, text")
    prize_value = models.CharField(max_length=200, null=True, blank=True, verbose_name="Il premio es. 30, una pizza, ...")
    extra_prize_value = models.CharField(max_length=200, null=True, blank=True, verbose_name="E' un premio extra per alcuni eventi, per esempio nell'evento 'proponici un amico' è il premio che riceverà l'amico")
    start_delay = models.IntegerField(null=True, blank=True, verbose_name="L'evento viene spedito se l'utente è creato da almeno questi giorni")
    repeat_delay = models.IntegerField(null=True, blank=True, verbose_name="Dopo il primo invio, tutti i successivi sono ogni x giorni, indicati da questo numero")
    extra_text = models.TextField(null=False, blank=True, verbose_name="Testo aggiuntivo, es. le limitazioni dei coupon per questo evento")
    channels_bitmask = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name="Indica su quali canali inviare l'evento, per il momento esiste solo il channel email")
    ma_event_type = models.CharField(max_length=30, null=False, blank=False, choices=MA_EVENT_TYPE, verbose_name="Il tipo di ma event, se solo premio, tickle+premio oppure schedulato nel tempo")
    json_params = JSONField(null=True, blank=True, verbose_name="Parametri aggiuntivi per l'evento in formato JSON")
    status = models.BooleanField(default=0, verbose_name="Indica se l'evento è attivo o no (1=attivo, 0=non attivo)")

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return str(self.ma_event_id)

    def get_by_ma_code(self, ma_code):
        """Funtion to retrieve ma_event by ma_code"""
        return_var = None

        try:
            return_var = MaEvent.objects.values().get(ma_code=ma_code)
        except MaEvent.DoesNotExist:
            # la riga non esiste, mando una mail al developer
            logger.error("errore in get_by_ma_code, codice " + str(ma_code) + " non esistente")
            raise 

        return return_var

    def event_can_be_performed(self, ma_code, repeat_delay, user_id):
        """
        Se l'id dell'evento non è presente nella tabella ma_event_log posso inviare l'evento
        Se l'id dell'evento è presente nella tabella ma_event_log devo controllare che i giorni 
        della data dell'ultimo inserimento siano > dei giorni in repeat_delay
        """
        return_var = False

        # return_var = MaEventLog.objects.values('creation_date').filter(user__id=user_id, creation_date__gt=timezone.now()-datetime.timedelta(days=repeat_delay)).last()
        ma_event_log_obj = MaEventLog.objects.values('ma_event_log_id', 'creation_date').filter(user__id=user_id, ma_code=ma_code).order_by('-ma_event_log_id').first()
        logger.info("@@@ check se inviare l'evento (code=" + str(ma_code) + ") @@@")
        if ma_event_log_obj:
            logger.info("evento esistente, controllo le date, per lo user_id (" + str(user_id) + ")")
            logger.info(str(timezone.now().date()) + " >= " + str((ma_event_log_obj["creation_date"]+datetime.timedelta(days=repeat_delay)).date()))
            # controllo che la data dell'ultimo invio + i giorni di repeat dell'evento siano minori o uguali a now()
            if timezone.now().date() >= (ma_event_log_obj["creation_date"]+datetime.timedelta(days=repeat_delay)).date():
                logger.info("evento esistente, date controllate -> posso reinviare l'evento")
                return_var = True
            else:
                logger.info("evento esistente, date controllate -> NON reinvio ancora l'evento")
        else:
            # event_log non ancora esistente, posso inviare l'evento
            logger.info("evento non ancora esistente -> posso inviare l'evento")
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

    def create_event_strings(self, ma_code_dictionary, prize_type, strings_ma_code, values_dictionary={}):
        """
        Function to build event strings disctionary (subject, title and content)
        qui restituisco le label con ancora le variabili da sostitutire, es {{prize_value}}, {{name}}, ...
        i valori verranno sostituiti in un secondo momento.

        Per ottenere una stringa con le variabili sostituite:
        MkautoStrings.get_string(key=MkautoStrings.strings[strings_ma_code + "." + prize_type + ".subject"], values_dictionary=values_dictionary)
        i valori verranno sostituiti con return self.strings[key].format(**values_dictionary) <- vedere oggetto strings.py
        """

        # in base al tipo di evento ottengo il codice da utilizzare per le stringhe e per le immagini
        logger.info("strings_ma_code: " + str(strings_ma_code))
        if prize_type:
            str_key = strings_ma_code + "." + prize_type
        else:
            str_key = strings_ma_code

        # TODO
        # alcune eccezioni per il codice dell'immagine
        image_code = strings_ma_code
        if strings_ma_code == "friend_prize":
            image_code = "welcome_prize"
        if strings_ma_code == "manual_welcome_prize":
            image_code = "welcome_prize"

        # immagini per promo e tip random
        if ma_code_dictionary["ma_code"] == "random_promo":
            image_code = "random_promo"
        if ma_code_dictionary["ma_code"] == "random_tip":
            image_code = "random_tip"

        return {
            "subject" : self.create_first_name_string(string=MkautoStrings.get_string(key=str_key + ".subject", values_dictionary=values_dictionary), separator=', ', first_name=values_dictionary.get("first_name")),
            "title" : self.create_first_name_string(string=MkautoStrings.get_string(key=str_key + ".title", values_dictionary=values_dictionary), separator=',<br />', first_name=values_dictionary.get("first_name")),
            "content" : MkautoStrings.get_string(key=str_key + ".content", values_dictionary=values_dictionary),
            "call_to_action_title" : MkautoStrings.get_string(key=strings_ma_code + ".call_to_action.title", values_dictionary=values_dictionary),
            "call_to_action_label" : MkautoStrings.get_string(key=strings_ma_code + ".call_to_action.label", values_dictionary=values_dictionary),
            "call_to_action_url" : MkautoStrings.get_string(key=strings_ma_code + ".call_to_action.url", values_dictionary=values_dictionary),
            "image_code" : image_code,
        }

    def get_strings_ma_code(self, event_dictionary):
        """Function to retrieve text and images final ma_code"""
        ma_code = event_dictionary.get("ma_code")
        ma_event_type = event_dictionary.get("ma_event_type")

        if ma_event_type == "tip" or ma_event_type == "monthly_prize":
            # prelevo il codice del prossimo tip o del prossimo monthly_prize (dipende su quale evento sto lavorando)
            # es. monthly_prize_tires_promotion_for_summer or tip_tip_code1
            ma_code = ma_event_type + "_" + str(self.get_next_random_code_order(event_dictionary=event_dictionary))
        elif ma_event_type == "prize_tickle": 
            # appendo al codice la scritta "_tickle"
            ma_code = "tickle_" + ma_code

        return ma_code

    def create_first_name_string(self, string, separator, first_name=""):
        """
        Function to create title or subject string
        es. Subject: Name, welcome to ... or Welcome to ...
        es. Title: Name,<br /> welcome to ... or Welcome to ...
        separator can be: ', ' or ',<br />'
        """
        # create first name string
        return self.ucfirst(first_name + separator + string)

    def make_event(self, user_id, ma_code=None, strings_ma_code=None, ma_code_dictionary=None, force_prize=False, skip_log_check=False):
        """
        Function to send a prize
            - ma_code lo utilizzo solo se non ho già tutti i dati in ma_code_dictionary per fare una get by code,
              fatta la get_by_code inserisco i dati nel dizionario ma_code_dictionary

            1) Controllo se posso inviare l'evento. in base allo start/repeat delay e la tabella ma_event_log
            2) Inserisco una riga in ma_event_log
            3) Creo una riga in ma_event_code
            4) Genero i testi per la mail (oggetto, titolo e testo) in base al tipo di premio e all'evento
            5) Sostituisco ai testi le variabili
            5) Invio il premio (il codice generato in ma_event_code) all'utente via email
        """

        if not ma_code_dictionary:
            # faccio una get_by_ma_code e riempo il dizionario ma_code_dictionary
            ma_code_dictionary = self.get_by_ma_code(ma_code=ma_code)

        if not ma_code_dictionary:
            # problemi con il codice passato alla funzione
            raise MaEventsCodeDoesNotExistError

        logger.info("MaEvent info dict")
        logger.info(ma_code_dictionary)

        # TODO
        if not strings_ma_code:
            # se non è presente la stringa per i testi e le immagini la prelevo
            strings_ma_code=self.get_strings_ma_code(event_dictionary=ma_code_dictionary)

        # 1)
        # Controllo se l'evento può essere inviato
        if not skip_log_check: # alcuni eventi (quelli a seguito della call to action di un tickle) non devono fare il check dei log, altrimenti non verrebbero mai inviati
            if not self.event_can_be_performed(ma_code=strings_ma_code, repeat_delay=ma_code_dictionary["repeat_delay"], user_id=user_id):
                # l'evento non può essere inviato (perchè non ancora oltre il repeat_delay)
                return False

        # 2)
        # TODO
        # aggiungere una riga anche se l'evento è disabilitato per evitare che la scaletta temporale degli eventi si modifichi
        # L'evento può essere inviato, inserisco una riga in ma_event_log
        # quindi il check dello status va fatto dopo questa funzione e non esternamente nello script
        # NB: effettuando questa modifica verranno inseriti molti ma_event_log inutili (per quanto riguarda gli eventi disabilitati)
        ma_event_log_obj = self.add_event_log(user_id=user_id, ma_event_id=ma_code_dictionary["ma_event_id"], ma_code=strings_ma_code)

        if not ma_code_dictionary["status"]:
            # se l'evento non è attivo esco dalla funzione
            return False

        # prelevo le info dell'account
        account_obj = Account()
        account_info_dictionary = account_obj.get_user_data_as_dictionary(user_id=user_id)

        # 3)
        # Creo una riga in ma_event_code (ma solo se la tipologia di codice lo richiede)
        coupon_code = False
        if force_prize or ma_code_dictionary["ma_event_type"] == "prize" or ma_code_dictionary["ma_event_type"] == "monthly_prize" or ma_code_dictionary["ma_event_type"] == "scheduled":
            coupon_code = self.add_event_code(user_id=user_id, ma_event_id=ma_code_dictionary["ma_event_id"], ma_event_log_id=ma_event_log_obj.ma_event_log_id, ma_code=ma_code_dictionary["ma_code"])

        # 4)
        # Genero i testi per la mail (oggetto, titolo e testo) in base al tipo di premio e all'evento
        # creo il dizionario con le chiavi e i valori da sostituire nella mail, all'interno
        # della funzione "create_event_strings" se l'evento è "tickle" appendo al codice "_tickle"

        # inizio a generare le variabili da sostituire nelle stringhe
        values_dictionary = {
            "first_name" : account_info_dictionary["first_name"],
            "prize_val" : ma_code_dictionary["prize_value"],
            "account_code" : account_info_dictionary["account__account_code"],
            "user_id" : account_info_dictionary["id"],
            "account_code" : account_info_dictionary["account__account_code"],
            "extra_prize_value" : ma_code_dictionary["extra_prize_value"],
        }

        event_strings = self.create_event_strings(
            ma_code_dictionary=ma_code_dictionary,
            prize_type=ma_code_dictionary["prize_type"],
            strings_ma_code=strings_ma_code,
            values_dictionary=values_dictionary # chiavi con valori da sostituire nei testi
        )

        # 6) Creo la mail con i testi definitivi e invio la mail
        cur_date = datetime.now()
        formatted_cur_date = cur_date.strftime("%Y-%m-%d")
        email_context = {
            "subject" : event_strings["subject"] + " (" + formatted_cur_date + ")",
            "title" : event_strings["title"],
            "content" : event_strings["content"],
            "image_url" : settings.SITE_URL + "/static/website/img/mkauto_images/" + event_strings["image_code"] + ".png",
            "coupon_code" : coupon_code,
            "coupon_code_extra_text" : '<p class="text fallback-text" style="color:#333;font-family:\'sans-serif\', Helvetica, Arial;font-size:15px;font-weight:300;font-style:normal;letter-spacing:normal;line-height:35px;text-transform:none;text-align:left;padding:0;margin:0;">' + str("Questo coupon non è cumulabile con altre offerte e si applica al solo costo di manodopera." if coupon_code else "") + ("<br />" + ma_code_dictionary["extra_text"] if ma_code_dictionary["extra_text"] else "") + "</p>",
            "call_to_action_title" : event_strings["call_to_action_title"],
            "call_to_action_label" : event_strings["call_to_action_label"],
            "call_to_action_url" : event_strings["call_to_action_url"],
            "user_profile_url" : settings.SITE_URL + "/profilo/" + str(account_info_dictionary["id"]) + "/" + str(account_info_dictionary["account__account_code"]),
            "email_unsubscribe_url" : settings.SITE_URL + "/disiscriviti/" + str(account_info_dictionary["id"]) + "/" + str(account_info_dictionary["account__account_code"] + "/mkauto/"),
        }

        logger.info("@@@ email context @@@")
        logger.info(email_context)

        CustomEmailTemplate(email_name="mkauto_email", email_context=email_context, recipient_list=[account_info_dictionary["email"],])

        return { "user_id" : user_id, "coupon_code" : coupon_code, }

    def generate_random_code(self, depth=0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        # TODO
        if MaEventCode.objects.filter(code=random_code).exists():
            # than recall this function to generate a new ones
            if depth < 50:
                random_code = self.generate_random_code(depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        else:
            # il codice non esiste in db pertano può essere utilizzato
            pass

        return random_code

    def create_mkauto_defaults(self):
        """Function to create defaults about mkauto events"""

        # svuoto la tabella con i default
        MaEvent.objects.all().delete()

        # creo gli ma_codes
        if mkauto_consts.mkauto_default_values:
            for event_name in mkauto_consts.mkauto_default_values:
                ma_event_obj = MaEvent()
                ma_event_obj.ma_code = mkauto_consts.mkauto_default_values[event_name].get("ma_code")
                ma_event_obj.description = mkauto_consts.mkauto_default_values[event_name].get("description")
                ma_event_obj.prize_type = mkauto_consts.mkauto_default_values[event_name].get("prize_type")
                ma_event_obj.prize_value = mkauto_consts.mkauto_default_values[event_name].get("prize_value")
                ma_event_obj.start_delay = mkauto_consts.mkauto_default_values[event_name].get("start_delay")
                ma_event_obj.repeat_delay = mkauto_consts.mkauto_default_values[event_name].get("repeat_delay")
                ma_event_obj.extra_text = mkauto_consts.mkauto_default_values[event_name].get("extra_text")
                ma_event_obj.ma_event_type = mkauto_consts.mkauto_default_values[event_name].get("ma_event_type")
                # se presenti, inserisco l'extra prize
                if mkauto_consts.mkauto_default_values[event_name].get("extra_prize_value"):
                    ma_event_obj.extra_prize_value = mkauto_consts.mkauto_default_values[event_name].get("extra_prize_value")
                ma_event_obj.status = mkauto_consts.mkauto_default_values[event_name].get("status")
                ma_event_obj.save(force_insert=True)

        # creo i codici random
        if mkauto_consts.random_code_default_values:
            for random_code_row in mkauto_consts.random_code_default_values:
                ma_random_code = MaRandomCode()
                ma_random_code.random_code_type = random_code_row.get("random_code_type")
                ma_random_code.random_code = random_code_row.get("random_code")
                ma_random_code.order = random_code_row.get("order")
                ma_random_code.save(force_insert=True)

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

    def get_ma_events(self):
        """Function to retrieve a dictionary of all active events"""
        return_var = {}

        ma_events = MaEvent.objects.values()
        if ma_events:
            for val in ma_events:
                return_var[val["ma_code"]] = val

        return return_var

    def get_next_random_code_order(self, event_dictionary):
        """Function to retrieve next random code order"""
        # ma_event_obj.json_params = {"random_code" : {"order" : -1, "expiring_date" : timezone.now() + 30gg}

        logger.info("@@@ get_next_random_code_order @@@")
        # logger.info("event_dictionary: " + str(event_dictionary))
        if event_dictionary.get("json_params") is not None:
            random_order = int(event_dictionary.get("json_params", {}).get("random_code", {}).get("order", -1))
            # https://docs.djangoproject.com/en/1.11/ref/utils/#module-django.utils.dateparse
            expiring_date = parse_date(event_dictionary.get("json_params", {}).get("random_code", {}).get("expiring_date", str(timezone.now().date())))
            logger.info("esiste già un json salvato nella riga di ma_event")
            logger.info("random_order retrieved: " + str(random_order))
            logger.info("expiring_date retrieved: " + str(expiring_date))
        else:
            random_order = -1
            expiring_date = timezone.now().date()
            logger.info("NON esiste ancora un json salvato nella riga di ma_event")

        logger.info("if timezone.now() >= expiring_date")
        logger.info(str(timezone.now().date()) + " >= " + str(expiring_date))
        if timezone.now().date() >= expiring_date:
            logger.info("posso incrementare il valore perchè il tempo per questo codice è terminato")
            # posso incrementare il valore perchè il tempo per questo codice è terminato
            random_order += 1
            if not MaRandomCode.objects.filter(order=random_order, random_code_type=event_dictionary.get("ma_event_type")).exists():
                logger.info("ho superato il limite, il codice random non esiste, riparto dallo '0'")
                # ho superato il limite, il codice random non esiste, riparto dallo '0'
                random_order = 0

            # salvo in db il nuovo ordinamento con la relativa data di scadenza
            ma_event_obj = MaEvent.objects.get(pk=event_dictionary.get("ma_event_id"))
            # next code date
            next_code_date = str((timezone.now()+datetime.timedelta(days=event_dictionary.get("repeat_delay"))).date())
            if ma_event_obj.json_params is not None:
                logger.info("in db il json esiste -> lo aggiorno")
                logger.info("order: " + str(random_order))
                logger.info("expiring_date: " + str(next_code_date))
                # aggorno il json già esistente
                ma_event_obj.json_params["random_code"]["order"] = random_order
                ma_event_obj.json_params["random_code"]["expiring_date"] = next_code_date
            else:
                logger.info("in db il json NON esiste -> lo creo")
                logger.info("order: " + str(random_order))
                logger.info("expiring_date: " + str(next_code_date))
                # creo il json perchè ancora non esiste
                ma_event_obj.json_params = { "random_code" : { "order" : random_order, "expiring_date" : next_code_date } }

            ma_event_obj.save(force_update=True)

        # prelevo l'order code da utilizzare
        ma_random_code_obj = MaRandomCode.objects.get(order=random_order, random_code_type=event_dictionary.get("ma_event_type"))

        logger.info("random_code da utilizzare: " + str(ma_random_code_obj.random_code))

        return ma_random_code_obj.random_code

    # TODO
    def check_event_log_exists(self, user_id, ma_code):
        """Function to check if a code was already sent at least one time"""
        return_var = False
        ma_event_obj = self.get_by_ma_code(ma_code=ma_code)

        if ma_event_obj:
            ma_event_log_exists = MaEventLog.objects.filter(user__id=user_id, ma_event__ma_event_id=ma_event_obj["ma_event_id"]).exists()
            logger.info("@@@ check_event_log_exists @@@")
            if ma_event_log_exists:
                logger.info("l'evento (" + str(ma_code) + ") è già stato inviato almeno una volta all'utente (user_id=" + str(user_id) + ")")
                return_var = True
            else:
                logger.info("l'evento (" + str(ma_code) + ") NON è mai stato inviato all'utente (user_id=" + str(user_id) + ")")

        return return_var

    # TODO
    def get_event_generic_prize_str(self, ma_code):
        """Function to retrieve event generic prize string"""
        return_var = ""
        ma_event_obj = self.get_by_ma_code(ma_code=ma_code)

        if ma_event_obj:
            return_var = MkautoStrings.get_string(key="generic_event." + str(ma_event_obj["prize_type"]) + ".text", values_dictionary={ "prize_val" : ma_event_obj["prize_value"] })

        return return_var

    # XXX: solo per uso interno di debug
    def delete_all_data(self):
        """Function to delete all data from ma_event tables"""
        MaEvent.objects.all().delete()
        MaEventLog.objects.all().delete()
        MaEventCode.objects.all().delete()
        MaRandomCode.objects.all().delete()

        return True

class MaEventLog(models.Model):
    ma_event_log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_maeventlog', on_delete=models.CASCADE)
    ma_event = models.ForeignKey(MaEvent, null=True, on_delete=models.SET_NULL)
    ma_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Codice identificativo dell'evento")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'mkauto_app'
        indexes = [
            models.Index(fields=['ma_code',]),
        ]

    def __unicode__(self):
        return str(self.ma_event_log_id)

class MaEventCode(models.Model):
    ma_event_code_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_maeventcode', on_delete=models.CASCADE)
    ma_event = models.ForeignKey(MaEvent, null=True, on_delete=models.SET_NULL)
    ma_event_log = models.ForeignKey(MaEventLog, on_delete=models.CASCADE)
    ma_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Codice identificativo dell'evento, il campo è duplicato (è già presente una chiave esterna di MaEvent), viene utilizzato a solo scopo informativo")
    code = models.CharField(max_length=15, null=False, blank=False)
    status = models.IntegerField(null=False, blank=False, default=1, verbose_name="Indica se il codice è utilizzato o no (1=non utilizzato 2=utilizzato)")
    creation_date = models.DateTimeField(default=timezone.now) # per poter modificare il campo anche nell'admin: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.DateField.auto_now_add
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'mkauto_app'
        indexes = [
            models.Index(fields=['code',]),
        ]

    def __unicode__(self):
        return str(self.ma_event_code_id)

    def get_by_code(self, code):
        """Function to retrieve MaEventCode instance by code"""
        try:
            # checking if code already exists
            ma_event_code_obj = MaEventCode.objects.get(code=code)
        except MaEventCode.DoesNotExist:
            # il codice non esiste in db
            raise

        return ma_event_code_obj

    def check_event_code_exists(self, code):
        """Function to check if a ma_event_code exists"""
        return MaEventCode.objects.filter(code=code).exists()

    # TODO
    def count_code_used(self, last_x_days=False):
	"""Function to count code used"""
	return_var = 0

	# conteggio solo gli utenti attivi (status=1) e che non siano staff (is_staff=False)
        return_var = MaEventCode.objects.filter(status=2)

        if last_x_days:
            # eventualmente solo degli ultimi x giorni
            return_var = return_var.filter(update_date__date__gte=(timezone.now()-datetime.timedelta(days=last_x_days)).date())

        return_var = return_var.count()

	return return_var

class MaRandomCode(models.Model):
    CODE_TYPE = (
        (mkauto_consts.random_code_type["tip"], mkauto_consts.random_code_type["tip"]),
        (mkauto_consts.random_code_type["monthly_prize"], mkauto_consts.random_code_type["monthly_prize"]),
    )
    ma_random_code_id = models.AutoField(primary_key=True)
    random_code_type = models.CharField(max_length=20, choices=CODE_TYPE, verbose_name="Il tipo di codice random (tip|monthly_prize)")
    random_code = models.CharField(max_length=50, null=False, blank=False, verbose_name="Il codice random identificativo, es. warning_light_prize")
    order = models.IntegerField(default=0, null=True, blank=True, verbose_name="L'ordinamento del codice random")

    class Meta:
        app_label = 'mkauto_app'
        unique_together = ("random_code", "order")

    def __unicode__(self):
        return str(self.ma_random_code_id)

class Feedback(models.Model):
    QUALITY_LEVEL = (
        (mkauto_consts.feedback_quality_code["excellent"]["quality_level"], mkauto_consts.feedback_quality_code["excellent"]["quality_code"]),
        (mkauto_consts.feedback_quality_code["very_good"]["quality_level"], mkauto_consts.feedback_quality_code["very_good"]["quality_code"]),
        (mkauto_consts.feedback_quality_code["average"]["quality_level"], mkauto_consts.feedback_quality_code["average"]["quality_code"]),
        (mkauto_consts.feedback_quality_code["low"]["quality_level"], mkauto_consts.feedback_quality_code["low"]["quality_code"]),
        (mkauto_consts.feedback_quality_code["very_bad"]["quality_level"], mkauto_consts.feedback_quality_code["very_bad"]["quality_code"]),
    )
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    quality_level = models.IntegerField(null=False, blank=False, choices=QUALITY_LEVEL, verbose_name="Qualità, es. 1,2,3,...")
    feedback_text = models.TextField(null=False, blank=False, verbose_name="Testo del feedback")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return str(self.feedback_id)

    def add_feedback(self, user_id, quality_level, feedback_text):
        """Function to add a new feedback"""
        new_feedback_obj = Feedback(
            user_id=user_id,
            quality_level=quality_level,
            feedback_text=feedback_text,
        )
        new_feedback_obj.save(force_insert=True)

        return new_feedback_obj

# TODO
class MasterAccountCode(models.Model):
    master_account_code_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, null=False, blank=False, unique=True, verbose_name="Codice di riferimento utente che propone amico")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return str(self.master_account_code_id)

    def create_or_get_master_code(self, user_id):
        """Function to create a master account code if not exists yet"""
        # checking if code already exists
        try:
            master_account_code_obj = MasterAccountCode.objects.get(user_id=user_id)
        except MasterAccountCode.DoesNotExist:
            master_account_code_obj = MasterAccountCode.objects.create(user_id=user_id, code=self.generate_random_code())

        return master_account_code_obj.code

    def get_by_code(self, code):
        """Function to retrieve MasterAccountCode instance by code"""
        try:
            # checking if code already exists
            ma_event_code_obj = MasterAccountCode.objects.get(code=code)
        except MasterAccountCode.DoesNotExist:
            # il codice non esiste in db
            raise

        return ma_event_code_obj

    def check_code_exists(self, code):
        """Function to check if a master code exists"""
        return MasterAccountCode.objects.filter(code=code).exists()

    def generate_random_code(self, depth=0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

        try:
            # checking if code already exists
            MasterAccountCode.objects.get(code=random_code)

            # than recall this function to generate a new ones
            if depth < 50:
                random_code = self.generate_random_code(self, depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        except MasterAccountCode.DoesNotExist:
            # il codice non esiste in db pertano può essere utilizzato
            pass

        return random_code

    # TODO
    def send_friend_invite(self, user_first_name, user_last_name, friend_first_name, friend_email, user_id):
        """Function to send an invite to a user's friend"""

        master_account_code_obj = MasterAccountCode()
        ma_event_obj = MaEvent()

        # creo la stringa del premio
        event_prize_str = ma_event_obj.get_event_generic_prize_str(ma_code="friend_prize")

        # creo o prelevo il codice affiliazione dell'account master
        aff_code = master_account_code_obj.create_or_get_master_code(user_id=user_id)

        email_subject = ma_event_obj.ucfirst(string=friend_first_name + ", " + user_first_name + " " + user_last_name + " ti invita a provare " + settings.SITE_NAME + ", ecco "  + str(event_prize_str))
        email_title = ma_event_obj.ucfirst(string=friend_first_name + ", " + user_first_name + " " + user_last_name + " ti invita a provare i servizi di " + settings.SITE_NAME + ",<br />ecco "  + str(event_prize_str))
        email_content = "Caro " + ma_event_obj.ucfirst(string=friend_first_name) + ", <b>" + user_first_name + " " + user_last_name + "</b> ti ha proposto di provare i servizi offerti da " + settings.SITE_NAME + ", ecco " + str(event_prize_str) + " per incentivarti.<br />Questi sono alcuni dei nostri servizi:<br />- Cambio olio e tagliando completo<br />- Manutenzione sistema frenante<br />- Sostituzione frizione<br />- Diagnosi elettronica<br />- Sostituzione / Riparazione gomme<br />...e molto altro, visita il nostro sito per scoprirli tutti.<br /><br /><b>Come fare per ricevere " + str(event_prize_str) + "?</b><br />Clicca sul pulsante sotto e registrati per ottenere subito il tuo sconto."

        email_context = {
            "subject" : email_subject,
            "title" : email_title,
            "content" : email_content,
            "image_url" : settings.SITE_URL + "/static/website/img/mkauto_images/tickle_friend_prize.png",
            "call_to_action_title" : "Clicca sul pulsante sotto<br />per ricevere subito il tuo sconto",
            "call_to_action_label" : "Ricevi lo sconto",
            "call_to_action_url" : "/ricevi-offerte/" + str(aff_code) + "/?fn=" + str(friend_first_name) + "&fe=" + str(friend_email),
        }

        logger.info("@@@ send_friend_invite email context @@@")
        logger.info(email_context)

        CustomEmailTemplate(email_name="mkauto_email", email_context=email_context, recipient_list=[friend_email,])

        return True

class FriendCode(models.Model):
    friend_code_id = models.AutoField(primary_key=True)
    master_account_code = models.ForeignKey(MasterAccountCode, on_delete=models.CASCADE)
    ma_event_code = models.ForeignKey(MaEventCode, on_delete=models.CASCADE)
    status = models.BooleanField(default=0, verbose_name="Indica se il codice è già stato utilizzato e quindi chi ha proposto l'amico ha ricevuto il premio (0=non utilizzato, 1=utilizzato)")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'mkauto_app'

    def __unicode__(self):
        return str(self.friend_code_id)

    def get_by_ma_event_code(self, ma_event_code_instance):
        """Function to retrieve FriendCode instance by ma_event_code_instance"""
        try:
            # checking if code already exists
            friend_code_obj = FriendCode.objects.get(ma_event_code=ma_event_code_instance)
        except FriendCode.DoesNotExist:
            # il codice non esiste in db
            raise

        return friend_code_obj

    def generate_friend_code(self, master_account_code, ma_event_code):
        """Function to generate a new friend code"""

        master_account_code_obj = MasterAccountCode()
        ma_event_code_obj = MaEventCode()
        if master_account_code_obj.check_code_exists(code=master_account_code) and ma_event_code_obj.check_event_code_exists(code=ma_event_code):
            # retrieve MaEventCode instance
            ma_event_code_instance = ma_event_code_obj.get_by_code(code=ma_event_code)
            # retrieve MasterAccountCode instance
            master_account_code_instance = master_account_code_obj.get_by_code(code=master_account_code)
            # creo la riga con match tra master_account_code e ma_event_code
            friend_code_obj = FriendCode.objects.create(master_account_code=master_account_code_instance, ma_event_code=ma_event_code_instance)
        else:
            raise MasterAccountCodeDoesNotExistsError

        return friend_code_obj
