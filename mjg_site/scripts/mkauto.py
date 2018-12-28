# -*- coding: utf-8 -*-

"""
https://django-extensions.readthedocs.io/en/latest/runscript.html

scripts/mkauto.py
script giornaliero per inviare gli eventi/tickle della mkauto
"""

from django.utils import timezone
from mkauto_app.models import MaEvent
from account_app.models import Account
from mjg_site.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def run():
    account_obj = Account()
    ma_event_obj = MaEvent()

    event_dictionary = ma_event_obj.get_ma_events()

    logger.info("@@@ event dictionary @@@")
    logger.info(event_dictionary)

    """
    Per ogni evento attivo:
    1) Prelevo le informazioni per l'evento
    2) Ottengo la lista di account validi per l'evento
    3) Ottengo il codice per le stringhe e le immagini
    4) Itero sull'elenco di account ed eseguo l'evento con "make_event"
    """

    # TODO
    # mettere lo user_id restituito dalla funzione  'make_event' in una lista
    # in modo da non inviare nello stesso giorno più notifiche ad eccezione di:
    # - notifica del compleanno
    # - notifiche stagionali (cambio gomme, tagliandi, ecc...)

    """
    # current week number
    week_day = (timezone.now()).date().weekday()

    if week_day == 0:
        # Lunedì
        # invio la promozione stagionale
    else :
        # tutti gli altri giorni della settimana
        # invio tutte le altre promozioni
    ##### Lasciaci la data di nascita per ricevere un bonus #####
    """

    ##### Bonus al compleanno {{{ #####
    current_ma_event = "happy_birthday_prize"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"), event_code=current_ma_event)
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Bonus al compleanno }}} #####

    ##### Bonus dicci la tua data di nascita per ottenere il bonus {{{ #####
    current_ma_event = "get_birthday_date"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"), event_code=current_ma_event)
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Bonus dicci la tua data di nascita per ottenere il bonus }}} #####

    ##### Chiedo all'utente di lasciare un feedback (informazioni interne) {{{ #####
    current_ma_event = "get_feedback"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"), event_code=current_ma_event)
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Chiedo all'utente di lasciare un feedback (informazioni interne) }}} #####

    ##### Chiedo all'utente di presentare degli amici {{{ #####
    current_ma_event = "refer_friend"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"))
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Chiedo all'utente di presentare degli amici }}} #####

    ##### Chiedo all'utente di lasciare una recensione (informazioni pubbliche) {{{ #####
    current_ma_event = "get_review"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"), event_code=current_ma_event)
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Chiedo all'utente di lasciare una recensione (informazioni pubbliche) }}} #####

    ##### Premio con un testo random  {{{ #####
    current_ma_event = "random_promo"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"))
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Premio con un testo random  }}} #####

    ##### Tip o info random {{{ #####
    current_ma_event = "random_tip"
    account_list = None
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")
    # 1) Prelevo le informazioni per l'evento
    single_event_dictionary = event_dictionary.get(current_ma_event, {})
    # 2) Ottengo la lista di account validi per l'evento
    account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"), event_code=None, bitmask_to_check=project_constants.RECEIVE_NEWSLETTERS_BITMASK)
    # 3) Ottengo il codice per le stringhe e le immagini
    strings_ma_code=ma_event_obj.get_strings_ma_code(event_dictionary=single_event_dictionary)
    # ottengo il codice per le stringhe e per le immagini
    if account_list:
        for single_account in account_list:
            ma_event_obj.make_event(user_id=single_account["id"], ma_code=current_ma_event, strings_ma_code=strings_ma_code, ma_code_dictionary=single_event_dictionary)
    ##### Tip o info random }}} #####
