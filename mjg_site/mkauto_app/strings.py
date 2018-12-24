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
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.title": "Per vedere il tuo profilo<br />clicca sul pulsante sotto",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.label": "Visualizza profilo",
        str(mkauto_consts.event_code["welcome_prize"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["welcome_prize"].get("prize_call_to_action", ""), # l'url contiene le variabili {user_id} e {account_code}
        # welcome_prize }}}
        # manual_welcome_prize {{{
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".discount.subject": "grazie per averci lasciato la tua email, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".bonus.subject": "grazie per averci lasciato la tua email, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".text.subject": "grazie per averci lasciato la tua email, ecco {prize_val}",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".discount.title": "grazie per averci lasciato la tua email,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".bonus.title": "grazie per averci lasciato la tua email,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".text.title": "grazie per averci lasciato la tua email, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".discount.content": "Complimenti e grazie per averci lasciato il tuo indirizzo email, ora che fai parte della nostra lista clienti privilegiata, potrai ricevere sconti, promozioni e consigli per la tua auto.<br />Subito per te ecco uno sconto del {prize_val}%.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".bonus.content": "Complimenti e grazie per averci lasciato il tuo indirizzo email, ora che fai parte della nostra lista clienti privilegiata, potrai ricevere sconti, promozioni e consigli per la tua auto.<br />Subito per te ecco un bonus di €{prize_val}.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".text.content": "Complimenti e grazie per averci lasciato il tuo indirizzo email, ora che fai parte della nostra lista clienti privilegiata, potrai ricevere sconti, promozioni e consigli per la tua auto.<br />Subito per te ecco {prize_val}.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".call_to_action.title": "Scopri i nostri servizi,<br />clicca sul pulsante sotto",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".call_to_action.label": "I nostri servizi",
        str(mkauto_consts.event_code["manual_welcome_prize"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["manual_welcome_prize"].get("prize_call_to_action", ""),
        # manual_welcome_prize }}}
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
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "Clicca sul pulsante sotto<br />per inserire la tua data di nascita",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "Inserisci data di nascita",
        str("tickle_" + mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["get_birthday_date"].get("tickle_call_to_action", ""), # l'url contiene le variabili {user_id} e {account_code}
        # evento
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.subject": "grazie per aver lasciato la tua data di nascita, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.subject": "grazie per aver lasciato la tua data di nascita, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.subject": "grazie per aver lasciato la tua data di nascita, ecco {prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.title": "grazie per aver lasciato la tua data di nascita,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.title": "grazie per aver lasciato la tua data di nascita,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.title": "grazie per aver lasciato la tua data di nascita, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".discount.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco uno sconto del {prize_val}%. Ti aspettiamo in officina ({business_address})",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".bonus.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco un bonus di €{prize_val}. Ti aspettiamo in officina ({business_address})",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".text.content": "Grazie per aver lasciato la tua data di nascita, ora potremo mandarti gli auguri con un regalo per il tuo compleanno, intanto nell'attesa, ecco {prize_val}. Ti aspettiamo in officina ({business_address})",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.title": "",
        str(mkauto_consts.event_code["get_birthday_date"]) + ".call_to_action.label": "",
        # get_birthday_date }}}
        # get_feedback {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.subject": "dai un parere al nostro servizio e riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.subject": "dai un parere al nostro servizio e riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.subject": "dai un parere al nostro servizio e riceverai {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.title": "dai un parere al nostro servizio,<br />riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.title": "dai un parere al nostro servizio,<br />riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.title": "dai un parere al nostro servizio e riceverai<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".discount.content": "Cosa pensi del nostro servizio?<br />Proponi qualche consiglio, suggerimenti o eventuali critiche e riceverai uno sconto del {prize_val}%.<br />Utilizzeremo le tue informazioni per offrirti un servizio ancora migliore.",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".bonus.content": "Cosa pensi del nostro servizio?<br />Proponi qualche consiglio, suggerimenti o eventuali critiche e riceverai un bonus di €{prize_val}.<br />Utilizzeremo le tue informazioni per offrirti un servizio ancora migliore.",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".text.content": "Cosa pensi del nostro servizio?<br />Proponi qualche consiglio, suggerimenti o eventuali critiche e riceverai {prize_val}.<br />Utilizzeremo le tue informazioni per offrirti un servizio ancora migliore.",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".call_to_action.title": "Per dare un parere al nostro servizio<br />clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".call_to_action.label": "Dai un parere al servizio",
        str("tickle_" + mkauto_consts.event_code["get_feedback"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["get_feedback"].get("tickle_call_to_action", ""), # l'url contiene le variabili {user_id} e {account_code}
        # evento
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.subject": "grazie per aver lasciato un parere sul nostro servizio, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.subject": "grazie per aver lasciato un parere sul nostro servizio, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.subject": "grazie per aver lasciato un parere sul nostro servizio, ecco {prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.title": "grazie per aver lasciato un parere sul nostro servizio,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.title": "grazie per aver lasciato un parere sul nostro servizio,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.title": "grazie per aver lasciato un parere sul nostro servizio, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_feedback"]) + ".discount.content": "Grazie per aver lasciato un parere sul nostro servizio, speriamo tu sia soddisfatto/a, in cambio ti offriamo questo sconto per le tue informazioni. Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["get_feedback"]) + ".bonus.content": "Grazie per aver lasciato un parere sul nostro servizio, speriamo tu sia soddisfatto/a, in cambio ti offriamo questo bonus per le tue informazioni. Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["get_feedback"]) + ".text.content": "Grazie per aver lasciato un parere sul nostro servizio, speriamo tu sia soddisfatto/a, in cambio ti offriamo questo regalo per le tue informazioni. Ti aspettiamo in officina ({business_address}).",
        # get_feedback }}}
        # refer_friend {{{
        # tickle
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.subject": "presentaci un amico, riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.subject": "presentaci un amico, riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.subject": "presentaci un amico, riceverai {prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.title": "presentaci un amico,<br />riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.title": "presentaci un amico,<br />riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.title": "presentaci un amico,<br />riceverai {prize_val}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".discount.content": "Speriamo che tu sia soddisfatto dei nostri servizi, per questo ti chiediamo di aiutarci a crescere, presentandoci un tuo amico, riceverete un premio entrambi.<br /><br /><b>Cosa riceverai tu</b>: uno sconto del {prize_val}%<br /><b>Cosa riceverà il tuo amico</b>: {extra_prize_value}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".bonus.content": "Speriamo che tu sia soddisfatto dei nostri servizi, per questo ti chiediamo di aiutarci a crescere, presentandoci un tuo amico, riceverete un premio entrambi.<br /><br /><b>Cosa riceverai tu</b>: un bonus di €{prize_val}<br /><b>Cosa riceverà il tuo amico</b>: {extra_prize_value}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".text.content": "Speriamo che tu sia soddisfatto dei nostri servizi, per questo ti chiediamo di aiutarci a crescere, presentandoci un tuo amico, riceverete un premio entrambi.<br /><br /><b>Cosa riceverai tu</b>: {prize_val}<br /><b>Cosa riceverà il tuo amico</b>: {extra_prize_value}",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".call_to_action.title": "Clicca sul pulsante sotto<br />per presentarci un amico",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".call_to_action.label": "Presentaci un amico",
        str("tickle_" + mkauto_consts.event_code["refer_friend"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["refer_friend"].get("tickle_call_to_action", ""),
        # evento
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.subject": "grazie per averci presentato un tuo amico, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.subject": "grazie per averci presentato un tuo amico, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.subject": "grazie per averci presentato un tuo amico, ecco {prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.title": "grazie per averci presentato un tuo amico,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.title": "grazie per averci presentato un tuo amico,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.title": "grazie per averci presentato un tuo amico, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["refer_friend"]) + ".discount.content": "Complimenti e grazie per averci presentato un tuo amico, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.<br />Presentaci altri amici per ricevere altri coupon di sconto.",
        str(mkauto_consts.event_code["refer_friend"]) + ".bonus.content": "Complimenti e grazie per averci presentato un tuo amico, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.<br />Presentaci altri amici per ricevere altri coupon di sconto.",
        str(mkauto_consts.event_code["refer_friend"]) + ".text.content": "Complimenti e grazie per averci presentato un tuo amico, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.<br />Presentaci altri amici per ricevere altri coupon di sconto.",
        str(mkauto_consts.event_code["refer_friend"]) + ".call_to_action.title": "Clicca sul pulsante sotto<br />per presentarci un altro amico",
        str(mkauto_consts.event_code["refer_friend"]) + ".call_to_action.label": "Presentaci un altro amico",
        str(mkauto_consts.event_code["refer_friend"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["refer_friend"].get("prize_call_to_action", ""),
        # evento
        str(mkauto_consts.event_code["friend_prize"]) + ".discount.subject": "grazie per la tua registrazione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["friend_prize"]) + ".bonus.subject": "grazie per la tua registrazione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["friend_prize"]) + ".text.subject": "grazie per la tua registrazione, ecco {prize_val}",
        str(mkauto_consts.event_code["friend_prize"]) + ".discount.title": "grazie per la tua registrazione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["friend_prize"]) + ".bonus.title": "grazie per la tua registrazione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["friend_prize"]) + ".text.title": "grazie per la tua registrazione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["friend_prize"]) + ".discount.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["friend_prize"]) + ".bonus.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["friend_prize"]) + ".text.content": "Complimenti, grazie alla tua registrazione su {website_name} riceverai sconti, promozioni e consigli per la tua auto.<br />Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["friend_prize"]) + ".call_to_action.title": "Scopri i nostri servizi,<br />clicca sul pulsante sotto",
        str(mkauto_consts.event_code["friend_prize"]) + ".call_to_action.label": "I nostri servizi",
        str(mkauto_consts.event_code["friend_prize"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["friend_prize"].get("prize_call_to_action", ""),
        # refer_friend }}}
        # get_review {{{
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.subject": "lasciaci una recensione, riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.subject": "lasciaci una recensione, riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.subject": "lasciaci una recensione, riceverai {prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.title": "lasciaci una recensione,<br />riceverai uno sconto del {prize_val}%",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.title": "lasciaci una recensione,<br />riceverai un bonus di €{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.title": "lasciaci una recensione, riceverai<br />{prize_val}",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".discount.content": "Sei soddisfatto/a dei nostri servizi? Aiutaci a crescere lasciandoci una recensione, in cambio riceverai uno sconto del {prize_val}%.",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".bonus.content": "Sei soddisfatto/a dei nostri servizi? Aiutaci a crescere lasciandoci una recensione, in cambio riceverai un bonus di €{prize_val}.",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".text.content": "Sei soddisfatto/a dei nostri servizi? Aiutaci a crescere lasciandoci una recensione, in cambio riceverai {prize_val}.",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".call_to_action.title": "Per lasciarci una recensione<br />clicca sul pulsante sotto",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".call_to_action.label": "Lasciaci una recensione",
        str("tickle_" + mkauto_consts.event_code["get_review"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["get_review"].get("tickle_call_to_action", ""),
        str(mkauto_consts.event_code["get_review"]) + ".discount.subject": "grazie per averci lasciato una recensione, ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_review"]) + ".bonus.subject": "grazie per averci lasciato una recensione, ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_review"]) + ".text.subject": "grazie per averci lasciato una recensione, ecco {prize_val}",
        str(mkauto_consts.event_code["get_review"]) + ".discount.title": "grazie per averci lasciato una recensione,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["get_review"]) + ".bonus.title": "grazie per averci lasciato una recensione,<br />ecco un bonus di €{prize_val}",
        str(mkauto_consts.event_code["get_review"]) + ".text.title": "grazie per averci lasciato una recensione, ecco<br />{prize_val}",
        str(mkauto_consts.event_code["get_review"]) + ".discount.content": "Complimenti e grazie per averci lasciato una recensione, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.",
        str(mkauto_consts.event_code["get_review"]) + ".bonus.content": "Complimenti e grazie per averci lasciato una recensione, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.",
        str(mkauto_consts.event_code["get_review"]) + ".text.content": "Complimenti e grazie per averci lasciato una recensione, ti aspettiamo in officina ({business_address}), ricordati di portare questo coupon.",
        str(mkauto_consts.event_code["get_review"]) + ".call_to_action.title": "Scopri i nostri servizi,<br />clicca sul pulsante sotto",
        str(mkauto_consts.event_code["get_review"]) + ".call_to_action.label": "I nostri servizi",
        str(mkauto_consts.event_code["get_review"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["get_review"].get("prize_call_to_action", ""),
        # get_review }}}
        # happy_birthday_prize {{{
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.subject": "buon compleanno, ecco il tuo regalo per questo giorno speciale",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.subject": "buon compleanno, ecco il tuo regalo per questo giorno speciale",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.subject": "buon compleanno, ecco il tuo regalo per questo giorno speciale",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.title": "buon compleanno, per festeggiare,<br />ecco uno sconto del {prize_val}%",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.title": "buon compleanno, per festeggiare,<br />ecco uno bonus di €{prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.title": "buon compleanno, per festeggiare,<br />ecco {prize_val}",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".discount.content": "Buon compleanno, per questa giornata speciale vogliamo farti un regalo.<br />Ecco sconto del {prize_val}% solo per te. Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".bonus.content": "Buon compleanno, per questa giornata speciale vogliamo farti un regalo.<br />Ecco un bonus di €{prize_val} solo per te. Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".text.content": "Buon compleanno, per questa giornata speciale vogliamo farti un regalo.<br />Ecco {prize_val} solo per te. Ti aspettiamo in officina ({business_address}).",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".call_to_action.title": "Scopri i nostri servizi,<br />clicca sul pulsante sotto",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".call_to_action.label": "I nostri servizi",
        str(mkauto_consts.event_code["happy_birthday_prize"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["happy_birthday_prize"].get("prize_call_to_action", ""),
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
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".subject": "ecco curiosità e trucchi sul mondo dei motori: spie auto, elenco completo e significati",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".title": "ecco curiosità e trucchi sul mondo dei motori: spie auto, elenco completo e significati",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".content": 'Le spie auto si illuminano con colori differenti in base al tipo di segnalazione: ci sono spie auto arancioni, spie gialle e spie rosse. Non mancano spie blu e bianche, anche se sono quelle legate a particolari comandi. Le spie blu possono segnalare l’attivazione dei fari abbaglianti, mentre le spie bianche fanno riferimento a diversi significati.<br /><br /><span style="display: inline-block; width: 100%; text-align: center;\ncolor:#333;font-family:\'sans-serif\', Helvetica, Arial;font-size:21px;font-weight:300;font-style:normal;letter-spacing:normal;line-height:35px;text-transform:none;padding:0;margin:0;"><b>Vediamo in dettaglio l\'elenco completo</b></span><br /><br /><img class="emailMainImage" src="{base_url}/static/website/img/tip_images/spie_auto.jpg" alt="Spie auto" style="display: block; height: auto; max-width: 99%; width: 100%;" border="0"><br />L’elenco che segue fa riferimento all’immagine delle spie auto in alto e ne riporta tutti i significati. Dalla spia della batteria alla tanto temuta spia avaria motore!<br /><br /><ol style="color:#333;font-family:\'sans-serif\', Helvetica, Arial;font-size:18px;font-weight:300;font-style:normal;letter-spacing:normal;line-height:35px;text-transform:none;text-align:left;margin:0;list-style: outside;list-style-type: decimal;padding-left: 24px;"><li>Fendinebbia frontali</li><li>Spia segnalazione del servosterzo</li><li>Fendinebbia posteriore</li>\n<li>Liquido per la pulizia dei cristalli scarso</li><li>Sostituire o controllare le pastiglie del freno</li><li>Cruise control attivo</li><li>Indicatori di direzione</li><li>Spia che avvisa di un malfunzionamento dei Sensori di pioggia e sensori luminosi</li><li>Modalità invernale</li><li>Indicatore per accedere alle info sul veicolo</li><li>Preriscaldamento delle candelette (spia candelette)</li><li>Rilevato ghiaccio su strada</li><li>Problema con l’interruttore di accensione</li><li>Chiave non rilevata nel veicolo</li><li>Sostituire la batteria delle chiavi</li><li>Distanza di sicurezza superata</li><li>Premere il pedale della frizione</li><li>Premere il pedale del freno</li><li>Spia che indica problemi al&nbsp;bloccosterzo</li><li>Spia dei fari abbaglianti attivati</li><li>Pressione degli pneumatici bassa</li><li>Fari attivi</li><li>Problemi ai gruppi ottici</li><li>Problemi alle luci di stop (luci posteriori)</li><li>Controllare o sostituire il filtro antiparticolato del diesel</li><li>Problemi al gancio traino del rimorchio</li>\n<li>Attenzione, malfunzionamento alle sospensioni</li><li>Lane Departure Warning (superamento della propria corsia)</li><li>Problemi al convertitore catalitico</li><li>Cinture di sicurezza non allacciate</li><li>Indicatore luminoso del freno di stazionamento, normale se appare per pochi secondi ma se resta fisso acceso indica problemi al sistema idraulico del freno</li><li>Problemi all’alternatore o alle batterie</li><li>Parking assist – sistema di assistenza al parcheggio attivo</li><li>Richiesta di assistenza</li><li>Luci adattive</li><li>Controllo della profondità del fascio luminoso dei fari</li><li>Problemi allo spoiler posteriore</li><li>Problemi alla capote</li><li>Mancato funzionamento dell’impianto air bag</li><li>Freno a mano attivo</li>\n<li>Rilevata acqua nel carburante</li><li>Airbag disattivato</li><li>Problemi generali, portare l’auto in assistenza</li><li>Luci anabbaglianti attive</li><li>Filtro dell’aria intasato</li><li>Modalità di guida&nbsp;<em>ECO&nbsp;</em>attivata</li><li>Hill Descent Control (HDC)</li><li>Problemi alla temperatura del liquido refrigerante del motore</li><li>Imprevisto al sistema ABS</li><li>Probabile problema al filtro del carburante</li><li>Porte aperte durante la marcia</li><li>Cofano motore aperto</li><li>I livelli di carburante hanno raggiunto la riserva</li><li>Automatic gearbox</li><li>Limitatore di velocità</li><li>Problemi agli ammortizzatori delle sospensioni</li>\n<li>Spia dell’olio motore accesa</li><li>Spia del disappannamento del parabrezza,&nbsp;quando accesa, indica che la ventilazione o il riscaldamento del parabrezza sono in funzione</li><li>Portellone posteriore aperto</li><li>Controllo di stabilità disattivato</li><li>Sensori di pioggia</li><li>Spia avaria motore</li><li>Spia del lunotto termico, indica che il sistema di sbrinamento è in azione.</li><li>Spazzole tergicristallo si attivano o disattivano automaticamente in funzione dei sensori di pioggia.</li></ol>\n',
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.title": "Scopri i nostri servizi,<br />clicca sul pulsante sotto",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.label": "I nostri servizi",
        str("tip_" + mkauto_consts.random_code["tip1"]) + ".call_to_action.url": mkauto_consts.mkauto_default_values["random_tip"].get("prize_call_to_action", ""),
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
        values_dictionary["base_url"] = str(settings.SITE_URL)

        logger.info("### values dictionary ###")
        logger.info(values_dictionary)
        logger.info("### key ###")
        logger.info(key)

        try:
            return MkautoStrings.strings.get(key).format(**values_dictionary)
        except AttributeError:
            return ""
