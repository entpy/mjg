# -*- coding: utf-8 -*-

from mkauto_app.consts import mkauto_consts
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

"""
In this module will be defined all strings about mkauto (subject, title and content)
"""
class MkautoStrings(object):
    strings = {
        # welcome_prize {{{
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.subject": "grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.subject": "grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.subject": "grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.title": "grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.title": "grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.title": "grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.content": "Testo per lo sconto {coupon_limitations}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.content": "Testo per il bonus {coupon_limitations}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.content": "Testo per il premio libero {coupon_limitations}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        str(mkauto_consts.event_code["welcome_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # welcome_prize }}}

        # TODO
        # inserire qui i testi aggiuntivi per gli altri eventi
    }

    @staticmethod
    def get_string(key, values_dictionary={}):
        """Function to retrieve mkauto string with replaced key"""
        # https://docs.python.org/3/library/string.html#string-formatting -> come tradurre i {blocco} in valore

        logger.info("### values dictionary ###")
        logger.info(values_dictionary)
        logger.info("### key ###")
        logger.info(key)

        try:
            return MkautoStrings.strings.get(key).format(**values_dictionary)
        except AttributeError:
            return ""
