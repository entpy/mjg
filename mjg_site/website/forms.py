# -*- coding: utf-8 -*-

from django import forms
from datetime import date
from django.conf import settings
from mkauto_app.consts import mkauto_consts
import calendar, locale, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# setting locale
locale.setlocale(locale.LC_ALL, settings.LOCALE)

class AccountForm(forms.Form):
    """Create a list of days for select element"""
    select_days_choices = []
    for i in range(1,32):
        select_days_choices.append((i, i))

    """Create a list of months for select element"""
    select_months_choices = []
    for i in range(1,13):
        select_months_choices.append((i, calendar.month_name[i].capitalize()))

    """Create a list of years for select element"""
    #                   current year - 18
    #                           |
    #                           V
    #for i in range(1960, (date.today().year - 17)):
    select_years_choices = []
    for i in range(1960, (date.today().year - 10)):
        select_years_choices.append((i, i))

    first_name = forms.CharField(label='Nome', max_length=30, required=True)
    last_name = forms.CharField(label='Cognome', max_length=30, required=False)
    email = forms.EmailField(label='Email', max_length=50, required=True)
    mobile_number = forms.CharField(label='Telefono', max_length=50, required=False)
    birthday_day = forms.ChoiceField(label='Giorno', choices=select_days_choices, required=False)
    birthday_month = forms.ChoiceField(label='Mese', choices=select_months_choices, required=False)
    birthday_year = forms.ChoiceField(label='Anno', choices=select_years_choices, required=False)

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Inserisci il tuo nome'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Inserisci il tuo cognome'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Inserisci la tua email'})
        self.fields['mobile_number'].widget.attrs.update({'placeholder': 'Inserisci il tuo numero di telefono'})

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        birthday_day = cleaned_data.get("birthday_day")
        birthday_month = cleaned_data.get("birthday_month")
        birthday_year = cleaned_data.get("birthday_year")

        # se ho inserito la data di nascita controllo che tutti e tre i campi siano inseriti

        if birthday_day or birthday_month or birthday_year:
            if not birthday_day or not birthday_month or not birthday_year:
            # Only do something if both fields are valid so far.
                raise forms.ValidationError("Data di nascita: devi specificare giorno, mese e anno")

class AccountNotifyForm(forms.Form):
    mkauto_input = forms.IntegerField(required=False)
    promotions_input = forms.IntegerField(required=False)
    newsletters_input = forms.IntegerField(required=False)

class FeedbackForm(forms.Form):
    QUALITY_LEVEL = (
        (mkauto_consts.feedback_quality_code["excellent"]["quality_level"], mkauto_consts.feedback_quality_code["excellent"]["quality_label"]),
        (mkauto_consts.feedback_quality_code["very_good"]["quality_level"], mkauto_consts.feedback_quality_code["very_good"]["quality_label"]),
        (mkauto_consts.feedback_quality_code["average"]["quality_level"], mkauto_consts.feedback_quality_code["average"]["quality_label"]),
        (mkauto_consts.feedback_quality_code["low"]["quality_level"], mkauto_consts.feedback_quality_code["low"]["quality_label"]),
        (mkauto_consts.feedback_quality_code["very_bad"]["quality_level"], mkauto_consts.feedback_quality_code["very_bad"]["quality_label"]),
    )
    feedback_text = forms.CharField(label='Cosa pensi del nostro servizio?', widget=forms.Textarea)
    quality_level = forms.ChoiceField(label='Qualità del servizio', choices=QUALITY_LEVEL, required=True)

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback_text'].widget.attrs.update({'placeholder': 'Scrivi qui consigli, suggerimenti o eventuali critiche...'})
