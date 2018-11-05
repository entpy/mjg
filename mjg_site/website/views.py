# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from mjg_site.exceptions import *
from website.forms import AccountForm
from account_app.models import Account
from mkauto_app.models import MaEvent
from django.views.decorators.csrf import ensure_csrf_cookie
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

    account_obj = Account()
    account_obj.get_mkauto_accounts(days_from_creation=10)

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
