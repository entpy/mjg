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
