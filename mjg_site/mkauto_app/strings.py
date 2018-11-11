# -*- coding: utf-8 -*-

from mkauto_app.consts import mkauto_consts
from django.conf import settings
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
        str(mkauto_consts.event_code["welcome_prize"]) + ".discount.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["welcome_prize"]) + ".bonus.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["welcome_prize"]) + ".text.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.title": "Per vedere il tuo profilo clicca sul pulsante sotto",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.label": "Visualizza profilo",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["welcome_prize"].get("prize_call_to_action", ""), # l'url contiene le variabili {user_id} e {account_code}
        # welcome_prize }}}
        # get_birthday_date {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.subject": "lasciaci la tua data di nascita, riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.subject": "lasciaci la tua data di nascita, riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.subject": "lasciaci la tua data di nascita, riceverai {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.title": "lasciaci la tua data di nascita,<br />riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.title": "lasciaci la tua data di nascita,<br />riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.title": "lasciaci la tua data di nascita, riceverai<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.content": "Lasciaci la tua data di nascita, così potremo mandarti gli auguri e un regalo per il tuo compleanno e...per non farti aspettare fino al tuo compleanno, ti daremo subito uno sconto del {prize_val}%.",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.content": "Lasciaci la tua data di nascita, così potremo mandarti gli auguri e un regalo per il tuo compleanno e...per non farti aspettare fino al tuo compleanno, ti daremo subito un bonus di €{prize_val}.",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.content": "Lasciaci la tua data di nascita, così potremo mandarti gli auguri e un regalo per il tuo compleanno e...per non farti aspettare fino al tuo compleanno, ti daremo subito {prize_val}.",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "Clicca sul pulsante sotto per inserire la tua data di nascita",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "Inserisci data di nascita",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["get_birthday_date"].get("tickle_call_to_action", ""), # l'url contiene le variabili {user_id} e {account_code}
        # evento
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.subject": "grazie per aver lasciato la tua data di nascita, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.subject": "grazie per aver lasciato la tua data di nascita, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.subject": "grazie per aver lasciato la tua data di nascita, ecco {prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.title": "grazie per aver lasciato la tua data di nascita,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.title": "grazie per aver lasciato la tua data di nascita,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.title": "grazie per aver lasciato la tua data di nascita, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco uno sconto del {prize_val}%.",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco un bonus di €{prize_val}.",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco {prize_val}.",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "",
        # get_birthday_date }}}
        # get_feedback {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.subject": "[tickle_get_feedback] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.subject": "[tickle_get_feedback] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.subject": "[tickle_get_feedback] grazie per la tua registrazione, ecco {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.title": "[tickle_get_feedback] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.title": "[tickle_get_feedback] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.title": "[tickle_get_feedback] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.content": "[tickle_get_feedback] Testo per lo sconto {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.content": "[tickle_get_feedback] Testo per il bonus {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.content": "[tickle_get_feedback] Testo per il premio libero {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".call_to_action.label": "Visualizza informazioni",
        # evento
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.subject": "[get_feedback] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.subject": "[get_feedback] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.subject": "[get_feedback] grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.title": "[get_feedback] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.title": "[get_feedback] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.title": "[get_feedback] grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.content": "[get_feedback] Testo per lo sconto {coupon_limitations}",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.content": "[get_feedback] Testo per il bonus {coupon_limitations}",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.content": "[get_feedback] Testo per il premio libero {coupon_limitations}",
        str(mkauto_consts.event_code["get_feedback"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str(mkauto_consts.event_code["get_feedback"]) + ".call_to_action.label": "Visualizza informazioni",
        # get_feedback }}}
        # refer_friend {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.subject": "[tickle_refer_friend] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.subject": "[tickle_refer_friend] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.subject": "[tickle_refer_friend] grazie per la tua registrazione, ecco {prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.title": "[tickle_refer_friend] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.title": "[tickle_refer_friend] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.title": "[tickle_refer_friend] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.content": "[tickle_refer_friend] Testo per lo sconto {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.content": "[tickle_refer_friend] Testo per il bonus {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.content": "[tickle_refer_friend] Testo per il premio libero {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".call_to_action.label": "Visualizza informazioni",
        # evento
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.subject": "[refer_friend] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.subject": "[refer_friend] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.subject": "[refer_friend] grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.title": "[refer_friend] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.title": "[refer_friend] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.title": "[refer_friend] grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.content": "[refer_friend] Testo per lo sconto {coupon_limitations}",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.content": "[refer_friend] Testo per il bonus {coupon_limitations}",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.content": "[refer_friend] Testo per il premio libero {coupon_limitations}",
        str(mkauto_consts.event_code["refer_friend"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str(mkauto_consts.event_code["refer_friend"]) + ".call_to_action.label": "Visualizza informazioni",
        # refer_friend }}}
        # get_review {{{
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.subject": "[tickle_get_review] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.subject": "[tickle_get_review] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.subject": "[tickle_get_review] grazie per la tua registrazione, ecco {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.title": "[tickle_get_review] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.title": "[tickle_get_review] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.title": "[tickle_get_review] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.content": "[tickle_get_review] Testo per lo sconto {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.content": "[tickle_get_review] Testo per il bonus {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.content": "[tickle_get_review] Testo per il premio libero {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".call_to_action.label": "Visualizza informazioni",
        # get_review }}}
        # happy_birthday_prize {{{
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.subject": "[happy_birthday_prize] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.subject": "[happy_birthday_prize] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.subject": "[happy_birthday_prize] grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.title": "[happy_birthday_prize] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.title": "[happy_birthday_prize] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.title": "[happy_birthday_prize] grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.content": "[happy_birthday_prize] Testo per lo sconto {coupon_limitations}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.content": "[happy_birthday_prize] Testo per il bonus {coupon_limitations}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.content": "[happy_birthday_prize] Testo per il premio libero {coupon_limitations}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        # happy_birthday_prize }}}
        # monthly_prize_warning_light_prize {{{
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".discount.subject": "[monthly_prize_warning_light_prize] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".bonus.subject": "[monthly_prize_warning_light_prize] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".text.subject": "[monthly_prize_warning_light_prize] grazie per la tua registrazione, ecco {prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".discount.title": "[monthly_prize_warning_light_prize] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".bonus.title": "[monthly_prize_warning_light_prize] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".text.title": "[monthly_prize_warning_light_prize] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".discount.content": "[monthly_prize_warning_light_prize] Testo per lo sconto {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".bonus.content": "[monthly_prize_warning_light_prize] Testo per il bonus {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".text.content": "[monthly_prize_warning_light_prize] Testo per il premio libero {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        # monthly_prize_warning_light_prize }}}
        # monthly_prize_light_burned_prize {{{
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".discount.subject": "[monthly_prize_light_burned_prize] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".bonus.subject": "[monthly_prize_light_burned_prize] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".text.subject": "[monthly_prize_light_burned_prize] grazie per la tua registrazione, ecco {prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".discount.title": "[monthly_prize_light_burned_prize] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".bonus.title": "[monthly_prize_light_burned_prize] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".text.title": "[monthly_prize_light_burned_prize] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".discount.content": "[monthly_prize_light_burned_prize] Testo per lo sconto {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".bonus.content": "[monthly_prize_light_burned_prize] Testo per il bonus {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".text.content": "[monthly_prize_light_burned_prize] Testo per il premio libero {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        # monthly_prize_light_burned_prize }}}
        # monthly_prize_noises_prize {{{
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".discount.subject": "[monthly_prize_noises_prize] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".bonus.subject": "[monthly_prize_noises_prize] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".text.subject": "[monthly_prize_noises_prize] grazie per la tua registrazione, ecco {prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".discount.title": "[monthly_prize_noises_prize] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".bonus.title": "[monthly_prize_noises_prize] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".text.title": "[monthly_prize_noises_prize] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".discount.content": "[monthly_prize_noises_prize] Testo per lo sconto {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".bonus.content": "[monthly_prize_noises_prize] Testo per il bonus {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".text.content": "[monthly_prize_noises_prize] Testo per il premio libero {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        # monthly_prize_noises_prize }}}
        # monthly_prize_bad_start_prize {{{
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".discount.subject": "[monthly_prize_bad_start_prize] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".bonus.subject": "[monthly_prize_bad_start_prize] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".text.subject": "[monthly_prize_bad_start_prize] grazie per la tua registrazione, ecco {prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".discount.title": "[monthly_prize_bad_start_prize] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".bonus.title": "[monthly_prize_bad_start_prize] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".text.title": "[monthly_prize_bad_start_prize] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".discount.content": "[monthly_prize_bad_start_prize] Testo per lo sconto {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".bonus.content": "[monthly_prize_bad_start_prize] Testo per il bonus {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".text.content": "[monthly_prize_bad_start_prize] Testo per il premio libero {coupon_limitations}",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".call_to_action.label": "Visualizza informazioni",
        # monthly_prize_bad_start_prize }}}
        # tip_tip1 {{{
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".subject": "[tip_tip1] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".title": "[tip_tip1] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".content": "[tip_tip1] Testo per lo sconto {coupon_limitations}",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.label": "Visualizza informazioni",
        # tip_tip1 }}}
        # tip_tip2 {{{
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".subject": "[tip_tip2] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".title": "[tip_tip2] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".content": "[tip_tip2] Testo per lo sconto {coupon_limitations}",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".call_to_action.label": "Visualizza informazioni",
        # tip_tip2 }}}


        "generic_event.discount.text": "uno sconto del {prize_val}%",
        "generic_event.bonus.text": "un bonus di €{prize_val}",
        "generic_event.text.text": "{prize_val}",

        # TODO
        # inserire qui i testi aggiuntivi per gli altri eventi
    }

    @staticmethod
    def get_string(key, values_dictionary={}):
        """Function to retrieve mkauto string with replaced key"""
        # https://docs.python.org/3/library/string.html#string-formatting -> come tradurre i {blocco} in valore

        # aggiungo alcune chiavi comuni a tutte le stringhe
        values_dictionary["website_name"] = str(settings.SITE_NAME)
        values_dictionary["business_address"] = str(settings.BUSINESS_ADDRESS)

        logger.info("### values dictionary ###")
        logger.info(values_dictionary)
        logger.info("### key ###")
        logger.info(key)

        try:
            return MkautoStrings.strings.get(key).format(**values_dictionary)
        except AttributeError:
            return ""
