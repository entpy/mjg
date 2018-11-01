# -*- coding: utf-8 -*-

from mkauto_app.consts import mkauto_consts
"""
In this module will be defined all strings about mkauto (subject, title and content)
"""
class mkauto_strings(object):
    strings = {
        # welcome_prize {{{
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.subject": "{{first_name}}grazie per la tua registrazione, ecco uno sconto del {{prize_val}}%",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.subject": "{{first_name}}grazie per la tua registrazione, ecco un bonus di €{{prize_val}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.subject": "{{first_name}}grazie per la tua registrazione, ecco {{prize_val}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.title": "{{first_name}}grazie per la tua registrazione,<br />ecco uno sconto del {{prize_val}}%",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.title": "{{first_name}}grazie per la tua registrazione,<br />ecco un bonus di €{{prize_val}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.title": "{{first_name}}grazie per la tua registrazione, ecco<br />{{prize_val}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.content": "Testo per lo sconto {{coupon_limitations}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.content": "Testo per il bonus {{coupon_limitations}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.content": "Testo per il premio libero {{coupon_limitations}}",
        str(mkauto_consts.event_code["welcome_prize"]) + ".prize_call_to_action.title": "Titolo della call to action",
        str(mkauto_consts.event_code["welcome_prize"]) + ".prize_call_to_action.label": "label call to action",
        str(mkauto_consts.event_code["welcome_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # welcome_prize }}}
        # TODO
        # aggiungere qui i testi aggiuntivi per gli altri eventi
    }
