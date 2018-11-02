# -*- coding: utf-8 -*-

"""
https://django-extensions.readthedocs.io/en/latest/runscript.html

scripts/mkauto.py
script giornaliero per inviare gli eventi/tickle della mkauto
"""

from email_app.models import MaEvent
from account_app.models import Account
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def run():
    """
        1) Ottengo un dizionario con tutti gli eventi e i valori di ogni evento
        2) Ottengo l'elenco di ogni utente per un dato evento
    """

    account_obj = Account()

    event_dictionary = ma_event_obj.get_active_ma_events()

    #logger.info("@@@ account list @@@")
    #logger.info(account_list)

    logger.info("@@@ event dictionary @@@")
    logger.info(event_dictionary)

    """
    Per ogni evento attivo:
    1) Prelevo le informazioni per l'evento
    2) Ottengo la lista di account validi per l'evento
    3) Itero sull'elenco di account ed eseguo l'evento con "make_event(user_id, ma_code=None, ma_code_dictionary=None, is_tickle=False)"
    """

    # TODO
    ##### Lasciaci la data di nascita per ricevere un bonus #####
    current_ma_event = "get_birthday_date"
    if event_dictionary.get(current_ma_event, {}).get("status"):
        logger.info("@@@ " + current_ma_event + " ATTIVO @@@")
        # 1) Prelevo le informazioni per l'evento
        single_event_dictionary = event_dictionary.get(current_ma_event, {})
        # 2) Ottengo la lista di account validi per l'evento
        account_list = account_obj.get_mkauto_accounts(days_from_creation=single_event_dictionary.get("start_delay"))
        if account_list:
            for single_account in account_list:
                ma_event_obj.make_event(user_id=single_account["id"], ma_code_dictionary=single_event_dictionary, is_tickle=True)
    else:
        logger.info("@@@ " + current_ma_event + " NON ATTIVO @@@")

    ##### Chiedo all'utente di lasciare un feedback (informazioni interne) #####
    if event_dictionary.get("get_feedback", {}).get("status"):
        logger.info("@@@ get_feedback ATTIVO @@@")
    else:
        logger.info("@@@ get_feedback NON ATTIVO @@@")

    ##### Premio con un testo random #####
    if event_dictionary.get("random_promo", {}).get("status"):
        logger.info("@@@ random_promo ATTIVO @@@")
    else:
        logger.info("@@@ random_promo NON ATTIVO @@@")

    ##### Chiedo all'utente di presentare degli amici #####
    if event_dictionary.get("refer_friend", {}).get("status"):
        logger.info("@@@ refer_friend ATTIVO @@@")
    else:
        logger.info("@@@ refer_friend NON ATTIVO @@@")

    ##### Chiedo all'utente di lasciare una recensione (informazioni pubbliche) #####
    if event_dictionary.get("get_review", {}).get("status"):
        logger.info("@@@ get_review ATTIVO @@@")
    else:
        logger.info("@@@ get_review NON ATTIVO @@@")

    ##### Bonus al compleanno #####
    if event_dictionary.get("happy_birthday_prize", {}).get("status"):
        logger.info("@@@ happy_birthday_prize ATTIVO @@@")
    else:
        logger.info("@@@ happy_birthday_prize NON ATTIVO @@@")

    return True
