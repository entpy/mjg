# -*- coding: utf-8 -*-

"""
In this module will be defined all strings about mkauto (subject, title and text)
"""
class mkauto_consts(object):
    event_code = {
        "welcome_prize" : "welcome_prize",
    }

    mkauto_default_values = [
        {
            "ma_code" : event_code["welcome_prize"],
            "prize_type" : "discount",
            "prize_value" : "30",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "is_tickle" : "0",
            # "channels_bitmask" : "",
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
    ]
