# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from background_task import background
from django.core import management

from django.shortcuts import render
# from django_ajax.decorators import ajax
from django.core.serializers.json import DjangoJSONEncoder

from mjg_site.exceptions import *
from mjg_site.common_utils import CommonUtils
# from website.forms import AccountForm, AccountNotifyForm, FeedbackForm, ReferFriendForm, ValidateCouponForm, ContactsForm, CampaignImageForm
from website.forms import *
from account_app.models import Account
from mkauto_app.models import MaEvent, Feedback, MasterAccountCode, FriendCode, MaEventCode
from promotion_app.models import *
from mkauto_app.strings import MkautoStrings
from mkauto_app.consts import mkauto_consts
from mjg_site.consts import project_constants
from email_app.email_core import CustomEmailTemplate
import datetime, logging, json

from django.contrib.auth.models import User
# Get an instance of a logger
logger = logging.getLogger(__name__)

def www_index(request):
    """View to show home page"""
    return render(request, 'website/www/www_index.html')

def www_services(request):
    """View to show services page"""
    return render(request, 'website/www/www_services.html')

def www_404(request):
    """View to show 404 page"""
    return render(request, 'website/www/www_404.html')

def www_500(request):
    """View to show 500 page"""
    return render(request, 'website/www/www_500.html')

@ensure_csrf_cookie
def www_contacts(request):
    """View to show contacts page"""

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ContactsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # invio una mail a info con la richiesta
            email_context = {
                "subject" : "Richiesta informazioni",
                "content" : "Nome: " + str(request.POST.get("first_name")) + "<br />Email: " + str(request.POST.get("email")) + "<br />Telefono: " + str(request.POST.get("mobile_number")) + "<br />Messaggio: " + str(request.POST.get("text")) + "<br />",
            }

            CustomEmailTemplate(email_name="blank_email", email_context=email_context, recipient_list=[settings.INFO_EMAIL_ADDRESS,], email_from=False, template_type="blank", reply_to=request.POST.get("email"))
            messages.add_message(request, messages.SUCCESS, "<h4>Richiesta inviata</h4><strong>La tua richiesta è stata correttamente inviata, ti risponderemo nel più breve tempo possibile<strong>.")
            return HttpResponseRedirect("/contattaci/")
        else:
            messages.add_message(request, messages.ERROR, "<h4>Ops...</h4><strong>Si sono verificati dei problemi, prova a ricaricare la pagina prima di un nuovo tentativo.</strong>")
            return HttpResponseRedirect("/contattaci/")

    return render(request, 'website/www/www_contacts.html')

@ensure_csrf_cookie
def www_get_offers(request, master_code=None, source=None):
    """View to show get offers page"""

    ma_event_obj = MaEvent()

    default_prize_code = "welcome_prize"
    if source == project_constants.SOURCE_FLYER_CHECKUP:
        # se sono arrivato dal flyer checkup uilizzo un altro codice premio
        default_prize_code = "welcome_prize2"

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                account_obj = Account()
                if master_code:
                    # se è presente un master_code l'utente proviene da un
                    # amico, quindi lo specifico nel source
                    form.cleaned_data["source"] = project_constants.SOURCE_REFER_FRIEND
                user_obj = account_obj.create_account(form.cleaned_data)
            except UserAlreadyExistsError:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, True)
            else:
                # creo e invio la mail di info ad admin
                cur_date = datetime.datetime.now()
                formatted_cur_date = cur_date.strftime("%d %B %Y")
                email_context = {
                    "subject" : "Registrazione di un nuovo cliente (" + formatted_cur_date + ")",
                    "title" : "Registrazione di un nuovo cliente",
                    "content" : "Complimenti, un nuovo cliente (" + str(user_obj.first_name) + " " + str(user_obj.email) + ") si è appena registrato sulla piattaforma, clicca sul link al fondo di questa email per andare nella pagina con le informazioni del nuovo cliente.<br /><a href='" + str(settings.SITE_URL) + "/dashboard/set-customer/" + str(user_obj.id) + "/'>Vedi cliente</a>",
                }

                CustomEmailTemplate(email_name="system_manage_email", email_context=email_context, recipient_list=[settings.INFO_EMAIL_ADDRESS,], email_from=False, template_type="admin")

                # invio l'evento (non controllo se l'evento è già stato inviato perchè qui finisco solo in caso di nuovo account)
                # se presente un master_code, sono nella registrazione di un amico del cliente, mando quindi il relativo bonus
                if master_code:
                    ma_event_return = ma_event_obj.make_event(user_id=user_obj.id, ma_code=mkauto_consts.event_code["friend_prize"], strings_ma_code=mkauto_consts.event_code["friend_prize"])
                    # l'utente proviene da un amico, aggiungo riga nella tabella 
                    friend_code_obj = FriendCode()
                    friend_code_obj.generate_friend_code(master_account_code=master_code, ma_event_code=ma_event_return["coupon_code"])
                    # creo messaggio di successo
                    success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["friend_prize"]) + " ti è stato inviato via email.<br />PS: <u>se utilizzi Gmail</u> prova a guardare nel tab \"Promozioni\""
                    messages.add_message(request, messages.SUCCESS, "<h4>Grazie per esserti registrato</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")
                    return HttpResponseRedirect("/ricevi-offerte/" + str(master_code))
                else:
                    ma_event_obj.make_event(user_id=user_obj.id, ma_code=mkauto_consts.event_code[default_prize_code], strings_ma_code=mkauto_consts.event_code[default_prize_code])
                    # creo messaggio di successo
                    success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code[default_prize_code]) + " ti è stato inviato via email<br />PS: <u>se utilizzi Gmail</u> prova a guardare nel tab \"Promozioni\""
                    messages.add_message(request, messages.SUCCESS, "<h4>Grazie per esserti registrato</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")
                    # redirect to a new URL:
                    if source == project_constants.SOURCE_FLYER_30:
                        return HttpResponseRedirect("/volantino/")
                    elif source == project_constants.SOURCE_FLYER_CHECKUP:
                        return HttpResponseRedirect("/offerta/")
                    else:
                        return HttpResponseRedirect("/ricevi-offerte/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

    if master_code:
            # prelevo la stringa del premio in caso di amico
            title_mkauto_prize_str = ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["friend_prize"])
            mkauto_prize = "Se ti registri, riceverai subito un coupon con " + str(title_mkauto_prize_str) + " da utilizzare presso di noi."
    else:
            # prelevo la stringa del premio in caso di welcome_bonus
            title_mkauto_prize_str = ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code[default_prize_code])
            mkauto_prize = "Se ti registri, riceverai subito un coupon con " + str(title_mkauto_prize_str) + " da utilizzare presso di noi."

    context = {
        "post" : request.POST,
        "form" : form,
        "master_code" : master_code,
        "mkauto_prize" : mkauto_prize,
        "title_mkauto_prize_str" : "Ottieni " + title_mkauto_prize_str,
        "friend_name" : request.GET.get("fn", ""),
        "friend_email" : request.GET.get("fe", ""),
        "source" : source,
    }

    return render(request, 'website/www/www_get_offers.html', context)

def www_mechanics(request):
    """View to show mechanics info page"""
    return render(request, 'website/www/www_mechanics.html')

def www_tires(request):
    """View to show tires info page"""
    return render(request, 'website/www/www_tires.html')

def www_checkup(request):
    """View to show checkup info page"""
    return render(request, 'website/www/www_tagliando_auto_torino.html')

# TODO
# nuovi {{{
def www_officina_autoriparazioni(request):
    """View to show www_officina_autoriparazioni page"""
    return render(request, 'website/www/www_officina_autoriparazioni.html')
def www_riparazioni_auto_epoca(request):
    """View to show www_riparazioni_auto_epoca page"""
    return render(request, 'website/www/www_riparazioni_auto_epoca.html')
def www_riparazione_auto_ibride_ed_elettriche(request):
    """View to show www_riparazione_auto_ibride_ed_elettriche page"""
    return render(request, 'website/www/www_riparazione_auto_ibride_ed_elettriche.html')
def www_vendita_montaggio_pneumatici(request):
    """View to show www_vendita_montaggio_pneumatici page"""
    return render(request, 'website/www/www_vendita_montaggio_pneumatici.html')
def www_cambio_stagionale_pneumatici(request):
    """View to show www_cambio_stagionale_pneumatici page"""
    return render(request, 'website/www/www_cambio_stagionale_pneumatici.html')
def www_custodia_pneumatici(request):
    """View to show www_custodia_pneumatici page"""
    return render(request, 'website/www/www_custodia_pneumatici.html')
def www_elettrauto(request):
    """View to show www_elettrauto page"""
    return render(request, 'website/www/www_elettrauto.html')
def www_tagliando_auto_torino(request):
    """View to show www_tagliando_auto_torino page"""
    return render(request, 'website/www/www_tagliando_auto_torino.html')
def www_ricarica_climatizzatore(request):
    """View to show www_ricarica_climatizzatore page"""
    return render(request, 'website/www/www_ricarica_climatizzatore.html')
def www_riparazione_climatizzatore(request):
    """View to show www_riparazione_climatizzatore page"""
    return render(request, 'website/www/www_riparazione_climatizzatore.html')
# nuovi }}}

def www_privacy_cookie_policy(request):
    """View to show privacy policy info page"""
    return render(request, 'website/www/www_privacy_cookie_policy.html')

def www_cookie_law(request):
    """View to show cookie law info page"""
    return render(request, 'website/www/www_cookie_law.html')

def www_directory(request):
    """View to show www_directory page"""
    return render(request, 'website/www/www_directory.html')

@ensure_csrf_cookie
def www_unsubscribe(request, user_id, account_code, unsubscribe_type):
    """View to show unsubscribe page"""

    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    if unsubscribe_type and (not unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_MKAUTO and not unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS and not unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS):
        # se il tipo di unsubscribe non esistesse tiro un 404
        raise Http404()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountNotifyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # salvo i dati validi nell'oggetto account
            account_bitmask = user_obj.account.notify_bitmask
            if unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_MKAUTO or unsubscribe_type is None:
                if form.cleaned_data.get("mkauto_input") == 1:
                    # aggiungo la bitmask
                    account_bitmask = user_obj.account.add_bitmask(bitmask=account_bitmask, add_value=project_constants.RECEIVE_MKAUTO_BITMASK)
                else:
                    # rimuovo la bitmask
                    account_bitmask = user_obj.account.remove_bitmask(bitmask=account_bitmask, remove_value=project_constants.RECEIVE_MKAUTO_BITMASK)
            if unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS or unsubscribe_type is None:
                if form.cleaned_data.get("promotions_input") == 1:
                    # aggiungo la bitmask
                    account_bitmask = user_obj.account.add_bitmask(bitmask=account_bitmask, add_value=project_constants.RECEIVE_PROMOTIONS_BITMASK)
                else:
                    # rimuovo la bitmask
                    account_bitmask = user_obj.account.remove_bitmask(bitmask=account_bitmask, remove_value=project_constants.RECEIVE_PROMOTIONS_BITMASK)
            if unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS or unsubscribe_type is None:
                if form.cleaned_data.get("newsletters_input") == 1:
                    # aggiungo la bitmask
                    account_bitmask = user_obj.account.add_bitmask(bitmask=account_bitmask, add_value=project_constants.RECEIVE_NEWSLETTERS_BITMASK)
                else:
                    # rimuovo la bitmask
                    account_bitmask = user_obj.account.remove_bitmask(bitmask=account_bitmask, remove_value=project_constants.RECEIVE_NEWSLETTERS_BITMASK)

            # logger.debug("new account bitmask: " + str(account_bitmask))
            save_data = { "notify_bitmask" : account_bitmask, }
            # salvo le modifiche
            user_obj.account.update_account(save_data=save_data, user_obj=user_obj)
            # creo messaggio di successo
            messages.add_message(request, messages.SUCCESS, True)
            # redirect to a new URL:
            return HttpResponseRedirect("/disiscriviti/" + str(user_id) + "/" + str(account_code) + "/" + str(unsubscribe_type or ""))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountNotifyForm()

    context = {
        "bitmask" : {
            project_constants.UNSUBSCRIBE_TYPE_MKAUTO : project_constants.RECEIVE_MKAUTO_BITMASK,
            project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS : project_constants.RECEIVE_PROMOTIONS_BITMASK,
            project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS : project_constants.RECEIVE_NEWSLETTERS_BITMASK
        },
        "account_notify" : {
            project_constants.UNSUBSCRIBE_TYPE_MKAUTO : account_obj.check_bitmask(user_obj.account.notify_bitmask, project_constants.RECEIVE_MKAUTO_BITMASK),
            project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS : account_obj.check_bitmask(user_obj.account.notify_bitmask, project_constants.RECEIVE_PROMOTIONS_BITMASK),
            project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS : account_obj.check_bitmask(user_obj.account.notify_bitmask, project_constants.RECEIVE_NEWSLETTERS_BITMASK)
        },
        "unsubscribe_type" : unsubscribe_type,
        "form" : form,
    }

    return render(request, 'website/www/www_unsubscribe.html', context)

@ensure_csrf_cookie
def www_profile(request, user_id, account_code, show_only_section):
    """View to show profile"""

    ma_event_obj = MaEvent()
    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    if show_only_section and not show_only_section == "bd":
        # se la sezione da mostrare non esistesse tiro un 404
        raise Http404()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)

        # se devo mostrare solo la sezione "data di nascita" setto alcuni campi come facoltativi
        # perchè non essendo mostrati nel form non mi permetterebbero di continuare con la validazione
        if show_only_section and show_only_section == "bd":
            form.fields['email'].required = False

        # check whether it's valid:
        if form.is_valid():
            # salvo i dati validi nell'oggetto account
            try:
                save_data = { }
                if show_only_section and show_only_section == "bd":
                    # salvo solo la data di nascita
                    save_data["first_name"] = form.cleaned_data["first_name"]
                    save_data["birthday_day"] = form.cleaned_data["birthday_day"]
                    save_data["birthday_month"] = form.cleaned_data["birthday_month"]
                    save_data["birthday_year"] = form.cleaned_data["birthday_year"]
                else:
                    # modifico l'intero profilo
                    save_data["first_name"] = form.cleaned_data["first_name"]
                    save_data["last_name"] = form.cleaned_data["last_name"]
                    save_data["email"] = form.cleaned_data["email"]
                    save_data["mobile_number"] = form.cleaned_data["mobile_number"]
                    save_data["birthday_day"] = form.cleaned_data["birthday_day"]
                    save_data["birthday_month"] = form.cleaned_data["birthday_month"]
                    save_data["birthday_year"] = form.cleaned_data["birthday_year"]
                # salvo le modifiche
                # posso modificare mail e telefono, a patto che non siano già stati inseriti
                user_obj.account.update_account(save_data=save_data, user_obj=user_obj)

            except UserAlreadyExistsError:
                # email e/o telefono già presenti
                messages.add_message(request, messages.ERROR, "I dati inseriti (email e/o telefono) sono già presenti")
            except UpdateUserDataError:
                # errore nel salvataggio dei dati
                messages.add_message(request, messages.ERROR, "Problema nel salvataggio dei dati, contatta l'amministratore")
            else:
                # creo messaggio di successo
                if show_only_section and show_only_section == "bd" and user_obj.account.birthday_date:
                    # il check farlo sul nuovo campo "get_birthday_date_event_done"
                    # se il premio non è ancora stato inviato, lo invio
                    # altrimenti non invio niente mostro il messaggio di successo normale, senza più bonus
                    # if not ma_event_obj.check_event_log_exists(user_id=user_id, ma_code=mkauto_consts.event_code["get_birthday_date"]):
                    if not user_obj.account.get_birthday_date_event_done:
                        # invio l'evento
                        ma_event_obj.make_event(user_id=user_id, ma_code=mkauto_consts.event_code["get_birthday_date"], strings_ma_code=mkauto_consts.event_code["get_birthday_date"], ma_code_dictionary=None, force_prize=True, skip_log_check=True)

                        # setto il campo 'get_birthday_date_event_done' dell'account a '1'
                        new_save_data = { "get_birthday_date_event_done" : "1" }
                        user_obj.account.update_account(save_data=new_save_data, user_obj=user_obj)

                        # creo messaggio di successo
                        success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_birthday_date"]) + " ti è stato inviato via email"
                        messages.add_message(request, messages.SUCCESS, "<h4>Grazie per aver inserito la tua data di nascita</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")
                    else:
                        messages.add_message(request, messages.SUCCESS, "I dati sono stati salvati con successo")
                else:
                    messages.add_message(request, messages.SUCCESS, "I dati sono stati salvati con successo")

                # redirect to a new URL:
                return HttpResponseRedirect("/profilo/" + str(user_id) + "/" + str(account_code) + "/" + str(show_only_section or ""))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

    # account_obj = Account()
    # account_obj.get_mkauto_accounts(days_from_creation=0)
    # prelevo la stringa del premio
    mkauto_prize = "lasciaci la tua data di nascita, riceverai " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_birthday_date"]) + "."
    title_mkauto_prize = "Ottieni " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_birthday_date"])

    context = {
        "post" : request.POST,
        "form": form,
        "user_info_dict" : user_obj,
        "show_only_section" : show_only_section,
        "birthday_day" : int(request.POST.get("birthday_day", user_obj.account.birthday_date.day if user_obj.account.birthday_date else 0)),
        "birthday_month" : int(request.POST.get("birthday_month", user_obj.account.birthday_date.month if user_obj.account.birthday_date else 0)),
        "birthday_year" : int(request.POST.get("birthday_year", user_obj.account.birthday_date.year if user_obj.account.birthday_date else 0)),
        "mkauto_prize" : ma_event_obj.create_first_name_string(string=mkauto_prize, separator=', ', first_name=user_obj.first_name),
        "title_mkauto_prize" : title_mkauto_prize,
    }

    return render(request, 'website/www/www_profile.html', context)

@ensure_csrf_cookie
def www_feedback(request, user_id, account_code):
    """View to show feedback page"""

    ma_event_obj = MaEvent()
    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # salvo il feedback
            feedback_obj = Feedback()
            feedback_obj.add_feedback(user_id=user_id, quality_level=form.cleaned_data["quality_level"], feedback_text=form.cleaned_data["feedback_text"])
            # se l'utente non ha ancora ricevuto il bonus lo invio
            if not user_obj.account.get_feedback_event_done:
                # invio l'evento
                ma_event_obj.make_event(user_id=user_id, ma_code=mkauto_consts.event_code["get_feedback"], strings_ma_code=mkauto_consts.event_code["get_feedback"], ma_code_dictionary=None, force_prize=True, skip_log_check=True)

                # setto il flag utente 'get_feedback_event_done' a 1
                new_save_data = { "get_feedback_event_done" : "1" }
                user_obj.account.update_account(save_data=new_save_data, user_obj=user_obj)

                # creo messaggio di successo
                success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_feedback"]) + " ti è stato inviato via email"
                messages.add_message(request, messages.SUCCESS, "<h4>Grazie per i tuoi preziosi consigli</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")
            else:
                messages.add_message(request, messages.SUCCESS, "Le informazioni sono state salvate con successo")
            # redirect to a new URL:
            return HttpResponseRedirect("/feedback/" + str(user_id) + "/" + str(account_code) + "/")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    # account_obj = Account()
    # account_obj.get_mkauto_accounts(days_from_creation=0)
    # prelevo la stringa del premio
    mkauto_prize = "cosa pensi del nostro servizio?<br />Dacci qualche consiglio, suggerimenti o eventuali critiche e riceverai " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_feedback"]) + "."

    context = {
        "post" : request.POST,
        "form": form,
        "user_info_dict" : user_obj,
        "mkauto_prize" : ma_event_obj.create_first_name_string(string=mkauto_prize, separator=', ', first_name=user_obj.first_name),
        "no_prize_string" : ma_event_obj.create_first_name_string(string="cosa pensi del nostro servizio?<br />Dacci qualche consiglio, suggerimento o eventuali critiche.", separator=', ', first_name=user_obj.first_name),
        "get_feedback_event_done" : user_obj.account.get_feedback_event_done,
    }

    return render(request, 'website/www/www_feedback.html', context)

@ensure_csrf_cookie
def www_refer_friends(request, user_id, account_code):
    """View to refer friends"""

    ma_event_obj = MaEvent()
    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    event_dictionary = ma_event_obj.get_ma_events()
    # prelevo i dati del codice della mkauto
    master_prize_dict = event_dictionary.get("refer_friend", {})
    friend_prize_dict = event_dictionary.get("friend_prize", {})

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReferFriendForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # se la mail inserita come amico è già presente in db blocco il processo
            if not account_obj.check_if_email_exists(email_to_check=form.cleaned_data["friend_email"]):
                # ora che ho anche il cognome, lo salvo nella riga dell'utente
                new_save_data = {
                    "first_name" : form.cleaned_data["account_first_name"],
                    "last_name" : form.cleaned_data["account_last_name"],
                    }
                user_obj.account.update_account(save_data=new_save_data, user_obj=user_obj)
                # mando una mail all'amico, con scritto di registrarsi per ottenere il bonus
                master_account_code_obj = MasterAccountCode()
                master_account_code_obj.send_friend_invite(user_first_name=form.cleaned_data["account_first_name"], user_last_name=form.cleaned_data["account_last_name"], friend_first_name=form.cleaned_data["friend_first_name"], friend_email=form.cleaned_data["friend_email"], user_id=user_id)
                # creo messaggio di successo
                messages.add_message(request, messages.SUCCESS, "<h4>Grazie per aver proposto un tuo amico</h4><strong>PS: avvisa il tuo amico che riceverà a breve una nostra email con le istruzioni per ricevere il bonus.</strong>")
            else:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, "<h4>Ops...</h4><strong>L'email inserita è già registrata, utilizza una email diversa.</strong>")

            # redirect to a new URL:
            return HttpResponseRedirect("/invita-amici/" + str(user_id) + "/" + str(account_code) + "/")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReferFriendForm()

    context = {
        "post" : request.POST,
        "form": form,
        "user_info_dict" : user_obj,
        "master_prize_val" : master_prize_dict.get("prize_value"),
        "friend_prize_val" : friend_prize_dict.get("prize_value"),
    }

    return render(request, 'website/www/www_refer_friends.html', context)

@ensure_csrf_cookie
def www_get_review(request, user_id, account_code):
    """View to write a review"""

    ma_event_obj = MaEvent()
    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)
    mkauto_assigned = user_obj.account.get_review_event_done

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    event_dictionary = ma_event_obj.get_ma_events()
    prize_dict = event_dictionary.get("get_review", {})
    mkauto_prize = "Riceverai " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_review"]) + "."

    if request.method == "POST":
        if request.POST.get("review_notify_form_sent") and not mkauto_assigned:
            # mando una mail ad admin e info con pulsante per inviare il bonus all'utente
            # NB: la verifica della recensione andrà fatta manualmente

            # creo e invio la mail
            email_context = {
                "subject" : "Un utente richiede il premio per aver lasciato la recensione su Google",
                "title" : "Un utente richiede il premio per aver lasciato la recensione su Google",
                "content" : "Clicca sul link al fondo di questa email per vedere le informazioni di chi ha lasciato la recensione e, dopo aver verificato che l'abbia fatto realmente, potrai assegnargli il bonus.<br /><a href='" + str(settings.SITE_URL) + "/dashboard/review-prize/" + str(user_id) + "/" + str(account_code) + "/'>Verifica recensione</a>",
            }

            CustomEmailTemplate(email_name="system_manage_email", email_context=email_context, recipient_list=[settings.INFO_EMAIL_ADDRESS,], email_from=False, template_type="admin")

            # creo messaggio di successo
            messages.add_message(request, messages.SUCCESS, "<h4>Grazie mille!</h4><strong>Grazie per averci scritto una recensione, ci aiuterà a crescere ed a rendere i nostri servizi ancora migliori.<br />Al termine della verifica invieremo il tuo bonus via email.</strong>")

            # redirect to a new URL:
            return HttpResponseRedirect("/lascia-una-recensione/" + str(user_id) + "/" + str(account_code) + "/")

    context = {
        "user_info_dict" : user_obj,
        "mkauto_prize" : mkauto_prize,
        "prize_val" : prize_dict.get("prize_value"),
        "mkauto_assigned" : mkauto_assigned,
    }

    return render(request, 'website/www/www_get_review.html', context)

@ensure_csrf_cookie
def www_promotion(request, camp_dest_code):
    """View to show campaign info"""

    campaign_obj = Campaign()
    campaign_order_obj = CampaignOrder()

    if not camp_dest_code:
        # se non sono riuscito a trovare una campagna tiro un 404
        raise Http404()

    # prelevo lo user_id, nel caso di un channel via URL non sarà presente
    campaign_dest_obj = campaign_obj.get_campaign_dest(campaign_dest_code=camp_dest_code)

    if not campaign_dest_obj:
        raise Http404()

    campaign_info_dict = campaign_obj.get_campaign_by_campaign_dest(campaign_dest_code=camp_dest_code)

    if not campaign_info_dict:
        # se non sono riuscito a trovare una campagna tiro un 404
        raise Http404()

    if request.method == "POST":
        # controllo se il campaign_order è già esistente oppure no, solo se è stato generato per un utente
        campaign_order_exists = False
        if campaign_dest_obj.get("user_id") and campaign_order_obj.get_campaign_order(campaign_id=campaign_dest_obj.get("campaign_id"), user_id=campaign_dest_obj.get("user_id")):
            campaign_order_exists = True

        # proveniente dalla view 'www_promotion'
        if request.POST.get("campaign_code_form_sent"):
            # ...altrimenti creo un codice promozionale per la campagna
            campaign_order_instance_obj = campaign_order_obj.get_or_create_campaign_order(campaign_id=campaign_dest_obj.get("campaign_id"), user_id=campaign_dest_obj.get("user_id"), dest=campaign_dest_obj.get("dest"))

            # MAIL AL CLIENTE
            # se il codice non esiste invio una mail ad admin e all'utente (se non è anonimo)
            if not campaign_order_exists and campaign_dest_obj.get("user_id"):
                campaign_obj.send_campaign_coupon(campaign_title=campaign_info_dict["camp_title"], campaign_order_code=campaign_order_instance_obj.code, campaign_image=campaign_info_dict["small_image_url"], user_id=campaign_dest_obj.get("user_id"))

            # MAIL AD ADMIN
            if not campaign_order_exists or campaign_dest_obj.get("dest") == "url":
                # identificazione dell'utente per la mail di admin
                user_text = "anonimo - proveniente dal canale " + campaign_dest_obj.get("dest")
                if campaign_dest_obj.get("user_id"):
                    user_text = str(campaign_order_instance_obj.user.first_name) + " " + str(campaign_order_instance_obj.user.email)

                # creo e invio la mail di info ad admin
                cur_date = datetime.datetime.now()
                formatted_cur_date = cur_date.strftime("%d %B %Y")
                admin_email_context = {
                    "subject" : "Prenotazione di un coupon (" + formatted_cur_date + ")",
                    "title" : "Un cliente ha prenotato un coupon",
                    "content" : "Complimenti, un cliente (" + str(user_text) + ") ha appena prenotato un coupon per la campagna: " + str(campaign_info_dict["camp_title"])
                }

                CustomEmailTemplate(email_name="system_manage_email", email_context=admin_email_context, recipient_list=[settings.INFO_EMAIL_ADDRESS,], email_from=False, template_type="admin")

            # redirect nella pagina per visualizzare il codice dell'ordine
            return HttpResponseRedirect("/p/" + str(camp_dest_code) + "/" + str(campaign_order_instance_obj.code) + "/")

    # se la campagna è scaduta mostro messaggio di errore
    if not campaign_obj.check_campaign_expiring(expiring_date=str(campaign_info_dict["expiring_date"])):
        return HttpResponseRedirect("/promozione-scaduta/")

    context = {
        "camp_dest_code" : camp_dest_code,
        "campaign_info_dict" : campaign_info_dict,
    }

    return render(request, 'website/www/www_promotion.html', context)

@ensure_csrf_cookie
def www_show_promo_code(request, camp_dest_code, camp_order_code):
    """View to retrieve campaign code"""

    campaign_obj = Campaign()
    campaign_order_obj = CampaignOrder()
    campaign_order_instance_obj = {}
    show_success_msg = False

    if not camp_dest_code or not camp_order_code:
        # se non sono riuscito a trovare una campagna tiro un 404
        raise Http404()

    # check campaign_dest
    campaign_dest_obj = campaign_obj.get_campaign_dest(campaign_dest_code=camp_dest_code)

    if not campaign_dest_obj:
        raise Http404()

    # check campaign_order
    campaign_order_instance_obj = campaign_order_obj.get_campaign_order_by_code(code=camp_order_code)

    if not campaign_order_instance_obj:
        raise Http404()

    # prelevo i dettagli della campagna
    campaign_info_dict = campaign_obj.get_campaign_by_campaign_dest(campaign_dest_code=camp_dest_code)

    # MAIL AL CLIENTE ANONIMO
    if request.method == "POST":
        if request.POST.get("send_coupon_form_sent") and request.POST.get("email"):
            # l'utente anonimo ha scelto di inviarsi il coupon via email
            campaign_obj.send_campaign_coupon(campaign_title=campaign_info_dict["camp_title"], campaign_order_code=campaign_order_instance_obj.code, campaign_image=campaign_info_dict["small_image_url"], user_id=False, user_email=request.POST.get("email"))

            # creo messaggio di successo
            messages.add_message(request, messages.SUCCESS, True)

            # redirect a questa pagina con messaggio di successo
            return HttpResponseRedirect("/p/" + str(camp_dest_code) + "/" + str(camp_order_code) + "/")

    # se è un cliente non anonimo mostro il messaggio di successo
    if campaign_order_instance_obj.user_id:
        show_success_msg = True

    # se è il channel URL mostro il form per inviare la mail con il coupon
    show_email_form = False
    if campaign_dest_obj.get("dest") == "url":
        show_email_form = True

    context = {
        "camp_dest_code" : camp_dest_code,
        "camp_order_code" : camp_order_code,
        "campaign_info_dict" : campaign_info_dict,
        "business_address" : settings.BUSINESS_ADDRESS,
        "show_success_msg" : show_success_msg,
        "show_email_form" : show_email_form,
    }

    return render(request, 'website/www/www_show_promo_code.html', context)

@ensure_csrf_cookie
def www_expired_promotion(request):
    """View to show expired promotion page"""

    return render(request, 'website/www/www_expired_promotion.html', {})

@login_required
@ensure_csrf_cookie
def dashboard_index(request):
    """View to show dashboard index"""

    account_obj = Account()
    ma_event_code_obj = MaEventCode()

    context = {
        "total_customers" : account_obj.count_total_account(),
        "total_customers_last_30_days" : account_obj.count_total_account(last_x_days=30),
        "total_codes" : ma_event_code_obj.count_code_used(),
        "total_codes_last_30_days" : ma_event_code_obj.count_code_used(last_x_days=30),
    }

    return render(request, 'website/dashboard/dashboard_index.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_customers(request):
    """View to show dashboard customers page"""

    if request.method == "POST":
        if request.POST.get("delete_customer_form_sent"):
            # elimino l'utente request.POST.get("customer_id")
            account_obj = Account()
            user_obj = account_obj.get_user_by_id(user_id=request.POST.get("customer_id"))

            if user_obj:
                # eliminazione soft (setto solo status=0)
                account_obj.user_hard_deletion(user_obj=user_obj)
                # creo messaggio di successo
                messages.add_message(request, messages.SUCCESS, "<h4>Eliminazione completata</h4>Il cliente è stato eliminato con successo")
            else:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, "<h4>Errore</h4>Errore durante l'eliminazione, cliente non trovato")

            # redirect to a new URL:
            return HttpResponseRedirect("/dashboard/customers/")

    return render(request, 'website/dashboard/dashboard_customers.html')

@login_required
@ensure_csrf_cookie
def dashboard_validate_coupon(request):
    """View to show dashboard validate coupons page"""

    common_utils_obj = CommonUtils()
    code_info_dict = {}

    if request.method == "POST":
        if request.POST.get("validate_code"):
            # valido il codice
            common_utils_obj.mark_code_as_used(code=request.POST.get("coupon_code"))
            messages.add_message(request, messages.SUCCESS, "<h4>Successo</h4>Il coupon è stato validato con successo.")
            return HttpResponseRedirect("/dashboard/validate-coupon/")
        else:
            # create a form instance and populate it with data from the request:
            form = ValidateCouponForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # check dell'esistenza del codice
                if common_utils_obj.check_code_exists(code=form.cleaned_data.get("coupon_code")):
                    # codice esistente, controllo se già utilizzato o no
                    if not common_utils_obj.check_code_used(code=form.cleaned_data.get("coupon_code")):
                        # codice non utilizzato, prelevo il contenuto del codice
                        code_info_dict = common_utils_obj.get_code_info(code=form.cleaned_data.get("coupon_code"))
                    else:
                        # codice già utilizzato
                        messages.add_message(request, messages.ERROR, "<h4>Errore</h4>Il coupon è già stato utilizzato.")
                else:
                    # codice non esistente
                    messages.add_message(request, messages.ERROR, "<h4>Errore</h4>Il coupon non esiste oppure è più vecchio di 12 mesi (quindi eliminato automaticamente).")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ValidateCouponForm()

    context = {
        "post" : request.POST,
        "form" : form,
        "code_info_dict" : code_info_dict,
    }
    return render(request, 'website/dashboard/dashboard_validate_coupon.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_review_prize(request, user_id, account_code):
    """View to assign a prize after review"""

    account_obj = Account()
    ma_event_obj = MaEvent()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    event_dictionary = ma_event_obj.get_ma_events()
    prize_dict = event_dictionary.get("get_review", {})
    mkauto_prize = ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_review"])

    if request.method == "POST":
        if request.POST.get("assign_review_prize_form_sent"):
            if not user_obj.account.get_review_event_done:
                # assegno il premio all'utente
                ma_event_obj.make_event(user_id=user_id, ma_code=mkauto_consts.event_code["get_review"], strings_ma_code=mkauto_consts.event_code["get_review"], ma_code_dictionary=None, force_prize=True, skip_log_check=True)

                # setto il flag utente 'get_review_event_done' a 1
                new_save_data = { "get_review_event_done" : "1" }
                user_obj.account.update_account(save_data=new_save_data, user_obj=user_obj)

                # redirect con messaggio di successo
                success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_review"]) + " è stato inviato all'utente via email"
                messages.add_message(request, messages.SUCCESS, "<h4>Premio inviato</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")

    context = {
        "user_info_dict" : user_obj,
        "mkauto_prize" : mkauto_prize,
        "mkauto_assigned" : user_obj.account.get_review_event_done,
        "user_id" : user_id,
    }

    return render(request, 'website/dashboard/dashboard_review_prize.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_set_customer(request, user_id):
    """View to show dashboard add/edit customer page"""

    ma_event_obj = MaEvent()
    account_obj = Account()

    user_obj = None
    birthday_day = 0
    birthday_month = 0
    birthday_year = 0
    if user_id:
        user_obj = account_obj.get_user_by_id(user_id=user_id)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                # se presente un id modifico i dati
                if user_id:
                    # modifico l'intero profilo
                    save_data = {}
                    save_data["first_name"] = form.cleaned_data["first_name"]
                    save_data["last_name"] = form.cleaned_data["last_name"]
                    save_data["email"] = form.cleaned_data["email"]
                    save_data["mobile_number"] = form.cleaned_data["mobile_number"]
                    save_data["birthday_day"] = form.cleaned_data["birthday_day"]
                    save_data["birthday_month"] = form.cleaned_data["birthday_month"]
                    save_data["birthday_year"] = form.cleaned_data["birthday_year"]
                    save_data["note"] = form.cleaned_data["note"]

                    account_obj.update_account(save_data, user_obj=user_obj, set_birthday_date_flag=True)
                else:
                    # creo un nuovo utente (verifico che email e/o telefono non siano già presenti)
                    form.cleaned_data["source"] = project_constants.SOURCE_MANUAL
                    user_obj = account_obj.create_account(form.cleaned_data)
            except UserAlreadyExistsError:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, "<h4>Controlla questi errori</h4>I dati inseriti (email e/o telefono) sono già presenti.")
            else:
                # check se inviare anche il manual welcome bonus
                if user_id:
                    # creo messaggio di successo
                    messages.add_message(request, messages.SUCCESS, "<h4>Cliente modificato</h4>I dati del cliente sono stati modificati correttamente.")
                else:
                    if request.POST.get("inputWelcomeBonus"):
                        # inviare il manual welcome bonus
                        ma_event_obj.make_event(user_id=user_obj.id, ma_code=mkauto_consts.event_code["manual_welcome_prize"], strings_ma_code=mkauto_consts.event_code["manual_welcome_prize"])
                        # creo messaggio di successo
                        messages.add_message(request, messages.SUCCESS, "<h4>Cliente salvato</h4>I dati del cliente sono stati correttamente salvati<br />Gli è stato anche inviato il bonus di benvenuto.")
                    else:
                        # creo messaggio di successo
                        messages.add_message(request, messages.SUCCESS, "<h4>Cliente salvato</h4>I dati del cliente sono stati salvati correttamente.")

                # redirect nella pagina del cliente
                return HttpResponseRedirect("/dashboard/set-customer/" + str(user_obj.id) + "/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

    # prelevo la stringa del premio in caso di welcome_bonus
    input_mkauto_label = "Invia al cliente anche: " + str(ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["manual_welcome_prize"]))

    if user_obj:
        birthday_day = int(request.POST.get("birthday_day", user_obj.account.birthday_date.day if user_obj.account.birthday_date else 0))
        birthday_month = int(request.POST.get("birthday_month", user_obj.account.birthday_date.month if user_obj.account.birthday_date else 0))
        birthday_year = int(request.POST.get("birthday_year", user_obj.account.birthday_date.year if user_obj.account.birthday_date else 0))

    context = {
        "post" : request.POST,
        "form" : form,
        "input_mkauto_label" : input_mkauto_label,
        "user_info_dict" : user_obj,
        "user_id" : user_id,
        "birthday_day" : birthday_day,
        "birthday_month" : birthday_month,
        "birthday_year" : birthday_year,
    }

    return render(request, 'website/dashboard/dashboard_set_customer.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_index(request):
    """View to show campaign index view"""

    context = {
    }

    return render(request, 'website/dashboard/campaigns/index.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_step1(request, campaign_id):
    """View to show create campaign flow"""

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CreateCampaignForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # creo/aggiorno la campagna
            save_data = { }
            save_data["camp_title"] = form.cleaned_data["camp_title"]
            save_data["was_price"] = form.cleaned_data["was_price"]
            save_data["final_price"] = form.cleaned_data["final_price"]
            save_data["camp_description"] = form.cleaned_data["camp_description"]
            save_data["small_image_id"] = form.cleaned_data["small_image_id"]
            save_data["large_image_id"] = form.cleaned_data["large_image_id"]
            save_data["campaign_type"] = project_constants.CAMPAIGN_TYPE_PROMOTION

            saved_campaign_obj = campaign_obj.create_update_campaign(data_dict=save_data, campaign_id=campaign_id)
            # redirect nello step2 con campaign_id
            return HttpResponseRedirect("/dashboard/campaigns/step2/" + str(saved_campaign_obj.campaign_id) + "/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateCampaignForm()

    context = {
        "post" : request.POST,
        "form" : form,
        "campaign_info_dict" : campaign_info_dict,
    }

    return render(request, 'website/dashboard/campaigns/step1.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_step2(request, campaign_id):
    """View to show create campaign flow"""

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SetCampaignExpiringForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # creo/aggiorno la campagna
            save_data = {}
            #camp_expiring_date = datetime.datetime.date(form.cleaned_data["expiring_date"])
            save_data["expiring_date"] = form.cleaned_data["expiring_date"]

            # test_date = timezone.localtime(form.cleaned_data["expiring_date"])
            # logger.info("tz data: " + str(test_date))
            # logger.info("data: " + str(form.cleaned_data["expiring_date"]))
            #camp_expiring_date = datetime.datetime.strptime(form.cleaned_data["expiring_date"], "%Y-%m-%d").date()

            saved_campaign_obj = campaign_obj.create_update_campaign(data_dict=save_data, campaign_id=campaign_id)
            # redirect nello step2 con campaign_id
            return HttpResponseRedirect("/dashboard/campaigns/step3/" + str(saved_campaign_obj.campaign_id) + "/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SetCampaignExpiringForm()

    context = {
        "post" : request.POST,
        "form" : form,
        "campaign_info_dict" : campaign_info_dict,
    }

    return render(request, 'website/dashboard/campaigns/step2.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_step3(request, campaign_id):
    """View to show create campaign flow"""

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    campaign_dest_obj = CampaignDest()

    # prelevo l'url della campagna
    campaign_url = campaign_dest_obj.get_campaign_url(campaign_id=campaign_id)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SetCampaignMessageTextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # creo/aggiorno la campagna
            save_data = { }
            save_data["msg_subject"] = form.cleaned_data["msg_subject"]
            save_data["msg_text"] = form.cleaned_data["msg_text"]

            saved_campaign_obj = campaign_obj.create_update_campaign(data_dict=save_data, campaign_id=campaign_id)
            # redirect nello step2 con campaign_id
            return HttpResponseRedirect("/dashboard/campaigns/step4/" + str(saved_campaign_obj.campaign_id) + "/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SetCampaignMessageTextForm()

    context = {
        "post" : request.POST,
        "form" : form,
        "campaign_url" : campaign_url,
        "campaign_info_dict" : campaign_info_dict,
    }

    return render(request, 'website/dashboard/campaigns/step3.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_step4(request, campaign_id):
    """View to show create campaign flow"""

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    # prelevo la lista di destinatari validi per la campagna
    account_obj = Account()
    campaign_user_temp_obj = CampaignUserTemp()
    # promotion|newsletter
    account_list = account_obj.get_campaign_accounts(campaign_type=project_constants.CAMPAIGN_TYPE_PROMOTION)

    # provo a precompilare la lista di destinatari temporanei
    valid_dest_list = campaign_user_temp_obj.get_sender_list_dict(campaign_id=campaign_id)

    if request.method == "POST":
        if request.POST.get("step4_form_sent") == "1":
            valid_dest_list = {}
            for single_dest in request.POST.getlist("selected_dest_account[]"):
                # inserisco l'utente nell'elenco dei destinatari
                valid_dest_list[int(single_dest)] = True
            # salvo l'elenco dei destinatari in campaign_user_temp
            campaign_user_temp_obj.create_sender_list(campaign_id=campaign_id, campaign_accounts=account_list, valid_dest_id_list=valid_dest_list)

            # redirect nello step5
            return HttpResponseRedirect("/dashboard/campaigns/step5/" + str(campaign_id) + "/")

    context = {
        "campaign_info_dict" : campaign_info_dict,
        "dest_account_list" : account_list,
        "valid_dest_list" : valid_dest_list,
    }

    return render(request, 'website/dashboard/campaigns/step4.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_campaigns_step5(request, campaign_id):
    """View to show create campaign flow"""

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    campaign_user_temp_obj = CampaignUserTemp()
    campaign_dest_obj = CampaignDest()

    # conteggio l'elenco dei destinatari
    count_campaign_sender = campaign_user_temp_obj.count_campaign_sender(campaign_id=campaign_id)

    # prelevo l'url della campagna
    campaign_url = campaign_dest_obj.get_campaign_url(campaign_id=campaign_id)

    if request.method == "POST":
        if request.POST.get("send_campaign") == "1":
            logger.info("chiamo lo script 'send_campaign'")
            # add new task in order to send a campaign
            send_campaign(campaign_id=campaign_id)
            # lancio il comando per eseguire i task schedulati
            # https://docs.djangoproject.com/en/1.11/ref/django-admin/#running-management-commands-from-your-code
            management.call_command('process_tasks', duration=1, interactive=False)

            # creo messaggio di successo
            messages.add_message(request, messages.SUCCESS, "<h4>Campagna inviata</h4>La campagna è stata inviata con successo, controlla le statistiche per vedere come funziona.")
            # redirect nella pagina delle promozioni
            return HttpResponseRedirect("/dashboard/campaigns/")

    context = {
        "campaign_info_dict" : campaign_info_dict,
        "count_campaign_sender" : count_campaign_sender,
        "campaign_url" : campaign_url,
    }

    return render(request, 'website/dashboard/campaigns/step5.html', context)

# TODO
@login_required
@ensure_csrf_cookie
def dashboard_campaigns_stats(request):
    """View to show stats page view"""

    campaign_obj = Campaign()
    campaign_list_working = []
    campaign_list_closed = []

    # TODO
    # eliminazione campagna
    if request.method == "POST":
        if int(request.POST.get("delete_campaign_form_sent")) == 1 and request.POST.get("campaign_id"):
            logger.info("elimino la campagna '" + str(request.POST.get("campaign_id")) + "'")
            campaign_obj.delete_campaign(campaign_id=request.POST.get("campaign_id"))

            messages.add_message(request, messages.SUCCESS, "<h4>Campagna eliminata</h4>La campagna è stata eliminata con successo.")

            # redirect nella pagina delle promozioni
            return HttpResponseRedirect("/dashboard/campaigns/stats/")

    # elenco delle campagne da completare
    campaign_list_working = campaign_obj.get_campaign_list(campaign_status=project_constants.CAMPAIGN_STATUS_IN_WORKING)

    # elenco delle campagne inviate
    campaign_list_closed = campaign_obj.get_campaign_list(campaign_status=project_constants.CAMPAIGN_STATUS_SENT)

    context = {
        "campaign_list_working" : campaign_list_working,
        "campaign_list_closed" : campaign_list_closed,
    }

    return render(request, 'website/dashboard/campaigns/stats.html', context)

@login_required
@ensure_csrf_cookie
def dashboard_single_campaign_stats(request, campaign_id):
    """View to show single campaign stats"""

    campaign_obj = Campaign()

    # se presente un id carico i dati della campagna (azione comune in tutto il flow della campagna) {{{
    campaign_obj = Campaign()
    campaign_info_dict = {}
    if campaign_id:
        campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_id=campaign_id)
    # }}}

    # prelevo le statistiche per la campagna 'campaign_id':
    # (email inviate - email aperte - email cliccate - coupon generati - coupon utilizzati)
    # (coupon generati channel url - coupon utilizzati channel url)
    campaign_stats_dict = campaign_obj.get_campaign_stats(campaign_id=campaign_id)

    context = {
        "campaign_stats_dict" : campaign_stats_dict,
        "campaign_info_dict" : campaign_info_dict,
    }

    return render(request, 'website/dashboard/campaigns/single_stats.html', context)

# ajax view {{{
# https://github.com/yceruto/django-ajax
@login_required
def ajax_customers_list(request):
    return_var = None
    account_obj = Account()

    # esempio di variabili passate via GET
    # search%5D=moto&sorts%5Blast_name%5D=1&page=1&perPage=10&offset=0
    # sorts[last_name]=-1
    # queries[search]=sdds
    # page=1
    # perPage=10
    # offset=0

    # prelevare il limite minimo e l'offset per la query (li ottengo dai parametri in GET)
    default_per_page = int(request.GET.get("perPage"))
    offset = int(request.GET.get("offset")) * 1
    page = int(request.GET.get("page")) * 1
    if offset == 0:
        query_offset = 0
        query_limit = default_per_page
    else:
        query_offset = offset
        query_limit = offset * page

    logger.info("### ajax_customers_list query_limit: " + str(query_limit))
    logger.info("### ajax_customers_list query_offset: " + str(query_offset))
    logger.info("### ajax_customers_list OFFSET: " + str(offset))
    logger.info("### ajax_customers_list SORTS: " + str(request.GET.get("sorts[first_name]")))
    logger.info("### ajax_customers_list SEARCH: " + str(request.GET.get("queries[search]")))

    # identifico eventuali ordinamenti
    sort_field = account_obj.sort_field_wrapper(request=request)

    # identifico eventuali ricerce del testo
    search_text = None
    if request.GET.get("queries[search]"):
        search_text = request.GET.get("queries[search]")

    account_queryset = account_obj.get_accounts(limit=query_limit, offset=query_offset, sort_field=sort_field, search_text=search_text)
    query_record_count = account_obj.get_accounts(limit=query_limit, offset=query_offset, sort_field=sort_field, search_text=search_text, only_count=True)
    count_total_accounts = account_obj.count_total_account()

    return_var = {
        "records": account_queryset,
        "queryRecordCount": query_record_count,
        "totalRecordCount": count_total_accounts if count_total_accounts > 0 else 0
    }

    return_var = json.dumps(return_var, cls=DjangoJSONEncoder)

    logger.info("### ajax_customers_list JSON " + str(return_var))

    # create http response (also attach a cookie if exists)
    return_var = HttpResponse(return_var, content_type="application/json")

    # return a JSON response
    return return_var

@login_required
@require_POST
def ajax_upload_campaign_image(request):
    return_var = None

    return_var = {
        "chiamata": "ajax_upload_campaign_image"
    }

    if request.method == 'POST':
        # form = CampaignImageForm(request.POST, request.FILES["camp_image"])
        #if form.is_valid():
        logger.info("image obj: " + str(request.FILES["camp_image"]))

        # saving small image
        CampaignImageSmall_obj = CampaignImage()
        CampaignImageSmall_obj.image = request.FILES["camp_image"]
        CampaignImageSmall_obj.size = "s"
        CampaignImageSmall_obj.save()

        # saving large image
        CampaignImageLarge_obj = CampaignImage()
        CampaignImageLarge_obj.image = request.FILES["camp_image"]
        CampaignImageLarge_obj.size = "l"
        CampaignImageLarge_obj.save()

        return_var = {
            "small_campaign_image_id": CampaignImageSmall_obj.campaign_image_id,
            "small_image_url": str(CampaignImageSmall_obj.image.url),
            "large_campaign_image_id": CampaignImageLarge_obj.campaign_image_id,
            "large_image_url": str(CampaignImageLarge_obj.image.url)
        }

    return_var = json.dumps(return_var, cls=DjangoJSONEncoder)

    logger.info("### ajax_upload_campaign_image JSON " + str(return_var))

    # create http response (also attach a cookie if exists)
    return_var = HttpResponse(return_var, content_type="application/json")

    # return a JSON response
    return return_var
# ajax view }}}

@login_required
def dashboard_create_mkauto_default(request):
    ma_event_obj = MaEvent()

    # per eliminare i dati già esistenti
    # if request.GET.get("clear_data"):
    #     ma_event_obj.delete_all_data()

    # creo i default della mkauto
    # solo se non ci sono ancora eventi salvati
    if MaEvent.objects.count() == 0:
        ma_event_obj.create_mkauto_defaults()
        return HttpResponse("Mkauto inizializzata con successo")
    else:
        return HttpResponse("Esistono già degli eventi, non faccio nulla")

# background actions {{{
@background(schedule=timezone.now())
def send_campaign(campaign_id):
    campaign_obj = Campaign()
    campaign_obj.send_campaign(campaign_id=campaign_id)

    return True
# background actions }}}
