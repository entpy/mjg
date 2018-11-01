# -*- coding: utf-8 -*-

"""
https://django-extensions.readthedocs.io/en/latest/runscript.html

scripts/mkauto.py
script giornaliero per inviare gli eventi/tickle della mkauto
"""

from email_app.models import MaEvent
from account_app.models import Account
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def run():
    """
        1) Ottengo un dizionario con tutti gli eventi e i valori di ogni evento
        2) Ottengo l'elenco di ogni utente per un dato evento
    """

    return True
