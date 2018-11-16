# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from mjg_site.exceptions import *
from website.forms import AccountForm, AccountNotifyForm, FeedbackForm, ReferFriendForm
from account_app.models import Account
from mkauto_app.models import MaEvent, Feedback
from mkauto_app.strings import MkautoStrings
from mkauto_app.consts import mkauto_consts
from mjg_site.consts import project_constants
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def www_index(request):
    """View to show home page"""
    return render(request, 'website/www/www_index.html')

def www_services(request):
    """View to show services page"""
    return render(request, 'website/www/www_services.html')

def www_contacts(request):
    """View to show contacts page"""
    return render(request, 'website/www/www_contacts.html')

def www_service_booking(request):
    """View to show service booking page"""
    return render(request, 'website/www/www_service_booking.html')

@ensure_csrf_cookie
def www_get_offers(request, unsubscribe_type):
    """View to show get offers page"""
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                account_obj = Account()
                user_obj = account_obj.create_account(form.cleaned_data)
            except UserAlreadyExistsError:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, True)
            else:
                # invio l'evento (non controllo se l'evento è già stato inviato perchè qui finisco solo in caso di nuovo account)
                ma_event_obj = MaEvent()
                ma_event_obj.make_event(user_id=user_obj.id, ma_code=mkauto_consts.event_code["welcome_prize"], strings_ma_code=mkauto_consts.event_code["welcome_prize"])
                # creo messaggio di successo
                success_msg_mkauto_prize = "Il coupon con " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["welcome_prize"]) + " ti è stato inviato via email"
                messages.add_message(request, messages.SUCCESS, "<h4>Grazie per esserti registrato</h4><strong>" + str(success_msg_mkauto_prize) + "</strong>.")
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('www_get_offers'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

    # account_obj = Account()
    # account_obj.get_mkauto_accounts(days_from_creation=0)

    context = {
        "post" : request.POST,
        "form": form,
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
    return render(request, 'website/www/www_checkup.html')

def www_privacy_cookie_policy(request):
    """View to show privacy policy info page"""
    return render(request, 'website/www/www_privacy_cookie_policy.html')

def www_cookie_law(request):
    """View to show cookie law info page"""
    return render(request, 'website/www/www_cookie_law.html')

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
                # TODO
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
                    # TODO
                    # il check farlo sul nuovo campo "get_birthday_date_event_done"
                    # se il premio non è ancora stato inviato, lo invio
                    # altrimenti non invio niente mostro il messaggio di successo normale, senza più bonus
                    # if not ma_event_obj.check_event_log_exists(user_id=user_id, ma_code=mkauto_consts.event_code["get_birthday_date"]):
                    if not user_obj.account.get_birthday_date_event_done:
                        # invio l'evento
                        ma_event_obj.make_event(user_id=user_id, ma_code=mkauto_consts.event_code["get_birthday_date"], strings_ma_code=mkauto_consts.event_code["get_birthday_date"], ma_code_dictionary=None, force_prize=True, skip_log_check=True)

                        # TODO
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

    context = {
        "post" : request.POST,
        "form": form,
        "user_info_dict" : user_obj,
        "show_only_section" : show_only_section,
        "birthday_day" : int(request.POST.get("birthday_day", user_obj.account.birthday_date.day if user_obj.account.birthday_date else 0)),
        "birthday_month" : int(request.POST.get("birthday_month", user_obj.account.birthday_date.month if user_obj.account.birthday_date else 0)),
        "birthday_year" : int(request.POST.get("birthday_year", user_obj.account.birthday_date.year if user_obj.account.birthday_date else 0)),
        "mkauto_prize" : ma_event_obj.create_first_name_string(string=mkauto_prize, separator=', ', first_name=user_obj.first_name),
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
    mkauto_prize = "cosa pensi del nostro servizio?<br />Dacci qualche consiglio, suggerimento o eventuali critiche e riceverai " + ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code["get_feedback"]) + "."

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

    account_obj = Account()
    user_obj = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_obj:
        # se non sono riuscito a tirare fuori l'utente mostro un 404
        raise Http404()

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReferFriendForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # TODO
            # ora che ho anche il cognome, lo salvo nella riga dell'utente
            new_save_data = { "first_name" : form.cleaned_data["account_first_name"] }
            user_obj.account.update_account(save_data=new_save_data, user_obj=user_obj)
            # TODO
            # mando una mail all'amico, con scritto di registrarai per ottenere il bonus
            master_account_code_obj = MasterAccountCode()
            master_account_code_obj.send_friend_invite(user_first_name=form.cleaned_data["account_first_name"], user_last_name=form.cleaned_data["account_last_name"], friend_first_name=form.cleaned_data["friend_first_name"], friend_email=form.cleaned_data["friend_email"], account_code=account_code)
            # TODO
            # creo messaggio di successo

            # redirect to a new URL:
            return HttpResponseRedirect("/invita-amici/" + str(user_id) + "/" + str(account_code) + "/")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReferFriendForm()

    context = {
        "post" : request.POST,
        "form": form,
        "user_info_dict" : user_obj,
    }

    return render(request, 'website/www/www_refer_friends.html', context)




def www_test_page(request):
    ma_event_obj = MaEvent()

    # XXX: debug only
    ma_event_obj.delete_all_data()

    # creo i default della mkauto
    ma_event_obj.create_mkauto_defaults()

    # ma_event_obj.add_event_log(user_id=20, ma_event_id=38)

    # provo ad eseguire un evento di test
    # ma_event_obj.make_event(user_id=20, ma_code="welcome_prize")

    # return HttpResponse("Test page!")
