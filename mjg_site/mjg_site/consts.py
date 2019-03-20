# -*- coding: utf-8 -*-

"""
In this module will be defined all constansts
"""
class project_constants(object):
    # notify bitmask {{{
    RECEIVE_MKAUTO_BITMASK = 1
    RECEIVE_PROMOTIONS_BITMASK = 2
    RECEIVE_NEWSLETTERS_BITMASK = 4

    UNSUBSCRIBE_TYPE_MKAUTO = "mkauto"
    UNSUBSCRIBE_TYPE_PROMOTIONS = "promotions"
    UNSUBSCRIBE_TYPE_NEWSLETTERS = "newsletters"
    # notify bitmask }}}

    # channels bitmask {{{
    CHANNEL_EMAIL = 1
    CHANNEL_SMS = 2
    # notify bitmask }}}

    # account source {{{
    SOURCE_UNDEFINED = ""
    SOURCE_MANUAL = 1
    SOURCE_GET_OFFERS = 2
    SOURCE_FLYER_30 = 3
    SOURCE_FLYER_CHECKUP = 4
    SOURCE_REFER_FRIEND = 5

    SOURCE = (
        (SOURCE_UNDEFINED, 'Indefinita'),
        (SOURCE_MANUAL, 'Caricamento manuale'),
        (SOURCE_GET_OFFERS, 'Pagina ricevi offerte'),
        (SOURCE_FLYER_30, 'Volantino sconto 30'),
        (SOURCE_FLYER_CHECKUP, 'Volantino checkup'),
        (SOURCE_REFER_FRIEND, 'Proposto da un amico'),
    )
    # account source }}}

    # campaigns {{{
    CAMPAIGN_TYPE_MKAUTO = "mkauto"
    CAMPAIGN_TYPE_PROMOTION = "promotion"
    CAMPAIGN_TYPE_NEWSLETTER = "newsletter"

    CAMPAIGN_STATUS_IN_WORKING = 1
    CAMPAIGN_STATUS_SENDING = 2
    CAMPAIGN_STATUS_SENT = 3
    CAMPAIGN_STATUS = (
        (CAMPAIGN_STATUS_IN_WORKING, 'In lavorazione'),
        (CAMPAIGN_STATUS_SENDING, 'In fase di invio'),
        (CAMPAIGN_STATUS_SENT, 'Inviata'),
    )

    CAMPAIGN_UPLOAD_DIR = "campaign_images/"
    # campaigns }}}
