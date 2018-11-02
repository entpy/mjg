# -*- coding: utf-8 -*-

"""
In this module will be defined all strings about mkauto (subject, title and text)
"""
class mkauto_consts(object):
    """
    random_tips = {
            1 : "warning_light_prize", # prize -> premio se hai una spia del cruscotto accesa
            2 : "light_burned_prize", # prize -> premio se hai una lampadina bruciata
            3 : "noises_prize", # prize -> premio se la tua auto fa dei rumori sospetti
            4 : "bad_start_prize", # prize -> premio se la tua auto si avvia con difficoltà
    }
    """
    ma_event_type = {
        "prize" : "prize", # premi diretti
        "random_prize" : "random_prize", # premi diretti
        "prize_tickle" : "prize_tickle", # mail di tickle e poi mail di premio se viene eseguito il tickle
        "scheduled" : "scheduled", # mail schedulate nel tempo (es. cambio gomme stagionale)
        "info" : "info", # email mensile di tip, non è una promozione ma un consiglio/curiosità sul mondo automobilistico
    }
    event_code = {
        # promozioni automatiche su flusso dell'utente
        # prize
            "welcome_prize" : "welcome_prize", # prize -> premio alla registrazione
            "happy_birthday_prize" : "happy_birthday_prize", # prize -> premio al compleanno
            "random_promo" : "random_promo", # prize -> premio al compleanno
            # random prize {{{
                #"""
                #"warning_light_prize" : "warning_light_prize", # prize -> premio se hai una spia del cruscotto accesa
                #"light_burned_prize" : "light_burned_prize", # prize -> premio se hai una lampadina bruciata
                #"noises_prize" : "noises_prize", # prize -> premio se la tua auto fa dei rumori sospetti
                #"bad_start_prize" : "bad_start_prize", # prize -> premio se la tua auto si avvia con difficoltà
                #"""
            # random prize }}}
        # tickle
            "get_birthday_date" : "get_birthday_date", # tickle -> premio per lasciare la data di nascita
            "get_feedback" : "get_feedback", # tickle -> per lasciare un feedback
            "get_review" : "get_review", # tickle -> per lasciare una recensione
            "refer_friend" : "refer_friend", # tickle -> per proporre un amico
        # promozioni automatiche basate sul tempo
            #"tires_promotion_for_summer" : "tires_promotion_for_summer", # cambio gomme per l'estate
            #"tires_promotion_for_winter" : "tires_promotion_for_winter", # cambio gomme per l'inverno
            #"services_promotion" : "services_promotion", # tagliando estivo stagionale
            #"air_conditioning_promotion" : "air_conditioning_promotion", # ricarica climatizzatore
        # TODO
        # tips and tricks
    }

    mkauto_default_values = [
        {
            "ma_code" : event_code["welcome_prize"],
            "description" : "Bonus alla registrazione di un utente",
            "prize_type" : "discount",
            "prize_value" : "30",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["get_birthday_date"],
            "description" : "Lasciaci la data di nascita per ricevere un bonus",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "7",
            "repeat_delay" : "112",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["get_feedback"],
            "description" : "Chiedo all'utente di lasciare un feedback (informazioni interne)",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "35",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["random_promo"],
            "description" : "Premio con un testo random",
            "prize_type" : "discount",
            "prize_value" : "10",
            "start_delay" : "49",
            "repeat_delay" : "56",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["random_prize"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["refer_friend"],
            "description" : "Chiedo all'utente di presentare degli amici",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "70",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["get_review"],
            "description" : "Chiedo all'utente di lasciare una recensione (informazioni pubbliche)",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "91",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["happy_birthday_prize"],
            "description" : "Bonus al compleanno",
            "prize_type" : "discount",
            "prize_value" : "10",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : mkauto_consts["prize"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        # TODO: mancano i tip mensili (mail senza codice)
        # TODO: mancano le promozioni basate sul tempo
    ]
