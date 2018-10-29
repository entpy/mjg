# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from website.forms import AccountForm
from account_app.models import Account
from django.views.decorators.csrf import ensure_csrf_cookie
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
def www_get_offers(request):
    """View to show get offers page"""
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AccountForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # TODO: salvo i dati validi nell'oggetto account
            # Account_obj = Account()
            # Account_obj.create_account(form.cleaned_data)

            # TODO creo messaggio di successo
            messages.add_message(request, messages.SUCCESS, True)
            # redirect to a new URL:
            return HttpResponseRedirect('/ricevi-offerte/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountForm()

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
