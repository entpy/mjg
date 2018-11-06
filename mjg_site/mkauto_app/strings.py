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
        # get_birthday_date {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.subject": "[tickle_get_birthday_date] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.subject": "[tickle_get_birthday_date] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.subject": "[tickle_get_birthday_date] grazie per la tua registrazione, ecco {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.title": "[tickle_get_birthday_date] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.title": "[tickle_get_birthday_date] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.title": "[tickle_get_birthday_date] grazie per la tua registrazione, ecco<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".discount.content": "[tickle_get_birthday_date] Testo per lo sconto {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".bonus.content": "[tickle_get_birthday_date] Testo per il bonus {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".text.content": "[tickle_get_birthday_date] Testo per il premio libero {coupon_limitations}",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "Visualizza informazioni",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # evento
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.subject": "[get_birthday_date] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.subject": "[get_birthday_date] grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.subject": "[get_birthday_date] grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.title": "[get_birthday_date] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.title": "[get_birthday_date] grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.title": "[get_birthday_date] grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.content": "[get_birthday_date] Testo per lo sconto {coupon_limitations}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.content": "[get_birthday_date] Testo per il bonus {coupon_limitations}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.content": "[get_birthday_date] Testo per il premio libero {coupon_limitations}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "Visualizza informazioni",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str(mkauto_consts.event_code["get_feedback"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str(mkauto_consts.event_code["refer_friend"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("monthly_prize_" + mkauto_consts.random_code["warning_light_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("monthly_prize_" + mkauto_consts.random_code["light_burned_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("monthly_prize_" + mkauto_consts.random_code["noises_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
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
        str("monthly_prize_" + mkauto_consts.random_code["bad_start_prize"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # monthly_prize_bad_start_prize }}}
        # tip_tip1 {{{
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".subject": "[tip_tip1] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".title": "[tip_tip1] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".content": "[tip_tip1] Testo per lo sconto {coupon_limitations}",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.label": "Visualizza informazioni",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # tip_tip1 }}}
        # tip_tip2 {{{
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".subject": "[tip_tip2] grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".title": "[tip_tip2] grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".content": "[tip_tip2] Testo per lo sconto {coupon_limitations}",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".call_to_action.title": "Per vedere le tue informazioni clicca sul pulsante sotto",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".call_to_action.label": "Visualizza informazioni",
        str("tip_" + mkauto_consts.random_code["tip2"]) + ".coupon_code_extra_text": "Presentaci questo coupon in sede per ottenere il bonus",
        # tip_tip2 }}}

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
