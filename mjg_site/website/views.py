# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from mjg_site.exceptions import *
from website.forms import AccountForm
from account_app.models import Account
from mkauto_app.models import MaEvent
from mjg_site.consts import project_constants
import logging

# TODO: solo per test, rimuovere
from django.http import HttpResponse

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
def www_get_offers(request):
    """View to show get offers page"""
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO: salvo i dati validi nell'oggetto account
            try:
                account_obj = Account()
                account_obj.create_account(form.cleaned_data)
            except UserAlreadyExistsError:
                # creo messaggio di errore
                messages.add_message(request, messages.ERROR, True)
            else:
                # creo messaggio di successo
                messages.add_message(request, messages.SUCCESS, True)
                # redirect to a new URL:
                return HttpResponseRedirect('/ricevi-offerte/')
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

# TODO
@ensure_csrf_cookie
def www_unsubscribe(request, user_id, account_code, unsubscribe_type):
    """View to show unsubscribe page"""
    # 1) Prelevo l'account associato
    # 2) Precompilo il form con i dati restituiti
    # 3) In base al tipo di unsubscribe mostro il form corretto

    # 1)
    # TODO: capire come fare a mostrare tutti gli unsubscribe se unsubscribe_type non viene passato
    account_obj = Account()
    user_dictionary = account_obj.get_user_by_id_account_code(user_id=user_id, account_code=account_code)

    if not user_dictionary:
        raise Http404()

    # 2)
    """
    if unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_MKAUTO:
    elif unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS:
    elif unsubscribe_type == project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS:
    """

    context = {
        "post" : request.POST,
        "bitmask" : {
            project_constants.UNSUBSCRIBE_TYPE_MKAUTO : project_constants.RECEIVE_MKAUTO_BITMASK,
            project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS : project_constants.RECEIVE_PROMOTIONS_BITMASK,
            project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS : project_constants.RECEIVE_NEWSLETTERS_BITMASK
        },
        "account_notify" : {
            project_constants.UNSUBSCRIBE_TYPE_MKAUTO : account_obj.check_bitmask(user_dictionary.account.notify_bitmask, project_constants.RECEIVE_MKAUTO_BITMASK),
            project_constants.UNSUBSCRIBE_TYPE_PROMOTIONS : account_obj.check_bitmask(user_dictionary.account.notify_bitmask, project_constants.RECEIVE_PROMOTIONS_BITMASK),
            project_constants.UNSUBSCRIBE_TYPE_NEWSLETTERS : account_obj.check_bitmask(user_dictionary.account.notify_bitmask, project_constants.RECEIVE_NEWSLETTERS_BITMASK)
        },
        "unsubscribe_type" : unsubscribe_type,
    }

    return render(request, 'website/www/www_unsubscribe.html', context)

def www_test_page(request):
    ma_event_obj = MaEvent()

    # XXX: debug only
    ma_event_obj.delete_all_data()

    # creo i default della mkauto
    ma_event_obj.create_mkauto_defaults()

    # ma_event_obj.add_event_log(user_id=20, ma_event_id=38)

    # TODO
    # provo ad eseguire un evento di test
    # ma_event_obj.make_event(user_id=20, ma_code="welcome_prize")

    return HttpResponse("Test page!")
