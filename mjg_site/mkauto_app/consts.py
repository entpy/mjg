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
        "monthly_prize" : "monthly_prize", # premi diretti
        "prize_tickle" : "prize_tickle", # mail di tickle e poi mail di premio se viene eseguito il tickle
        "scheduled" : "scheduled", # mail schedulate nel tempo (es. cambio gomme stagionale)
        "tip" : "tip", # email mensile di tip, non è una promozione ma un consiglio/curiosità sul mondo automobilistico
    }
    event_code = {
        # promozioni automatiche su flusso dell'utente
        # prize
            "welcome_prize" : "welcome_prize", # prize -> premio alla registrazione
            "manual_welcome_prize" : "manual_welcome_prize", # prize -> premio alla registrazione manuale
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
            "friend_prize" : "friend_prize", # tickle -> per proporre un amico
        # promozioni automatiche basate sul tempo
            #"tires_promotion_for_summer" : "tires_promotion_for_summer", # cambio gomme per l'estate
            #"tires_promotion_for_winter" : "tires_promotion_for_winter", # cambio gomme per l'inverno
            #"services_promotion" : "services_promotion", # tagliando estivo stagionale
            #"air_conditioning_promotion" : "air_conditioning_promotion", # ricarica climatizzatore
        # TODO
        # tips and tricks
        "random_tip" : "random_tip", # prize -> premio al compleanno
    }

    random_code_type = {
        "tip" : "tip",
        "monthly_prize" : "monthly_prize",
    }
    random_code = {
        # monthly_prize
        "warning_light_prize" : "warning_light_prize", # prize -> premio se hai una spia del cruscotto accesa
        "light_burned_prize" : "light_burned_prize", # prize -> premio se hai una lampadina bruciata
        "noises_prize" : "noises_prize", # prize -> premio se la tua auto fa dei rumori sospetti
        "bad_start_prize" : "bad_start_prize", # prize -> premio se la tua auto si avvia con difficoltà
        # tip (tip mensili)
        "tip1" : "tip1",
        "tip2" : "tip2",
    }

    random_code_default_values = [
        {
            "random_code_type" : random_code_type["monthly_prize"],
            "random_code" : random_code["warning_light_prize"],
            "order" : "0",
        },
        {
            "random_code_type" : random_code_type["monthly_prize"],
            "random_code" : random_code["light_burned_prize"],
            "order" : "1",
        },
        {
            "random_code_type" : random_code_type["monthly_prize"],
            "random_code" : random_code["noises_prize"],
            "order" : "2",
        },
        {
            "random_code_type" : random_code_type["monthly_prize"],
            "random_code" : random_code["bad_start_prize"],
            "order" : "3",
        },
        {
            "random_code_type" : random_code_type["tip"],
            "random_code" : random_code["tip1"],
            "order" : "0",
        },
        {
            "random_code_type" : random_code_type["tip"],
            "random_code" : random_code["tip2"],
            "order" : "1",
        },
    ]

    mkauto_default_values = {
        event_code["welcome_prize"] : {
            "ma_code" : event_code["welcome_prize"],
            "description" : "Bonus alla registrazione di un utente",
            "prize_type" : "discount",
            "prize_value" : "30",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize"],
            "prize_call_to_action" : "/profilo/{user_id}/{account_code}/",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        event_code["manual_welcome_prize"] : {
            "ma_code" : event_code["manual_welcome_prize"],
            "description" : "Bonus alla registrazione manuale di un utente",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize"],
            "prize_call_to_action" : "/servizi/",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        event_code["get_birthday_date"] : {
            "ma_code" : event_code["get_birthday_date"],
            "description" : "Lasciaci la data di nascita per ricevere un bonus",
            "prize_type" : "discount",
            "prize_value" : "20",
            "start_delay" : "7",
            "repeat_delay" : "112",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "/profilo/{user_id}/{account_code}/bd/",
            "status" : "1",
        },
        event_code["get_feedback"] : {
            "ma_code" : event_code["get_feedback"],
            "description" : "Chiedo all'utente di lasciare un feedback (informazioni interne)",
            "prize_type" : "discount",
            "prize_value" : "20",
            "start_delay" : "42",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "/feedback/{user_id}/{account_code}/",
            "status" : "1",
        },
        event_code["refer_friend"] : {
            "ma_code" : event_code["refer_friend"],
            "description" : "Chiedo all'utente di presentare degli amici",
            "prize_type" : "discount",
            "prize_value" : "25",
            "extra_prize_value" : "uno sconto del 20%", # l'unione del premio e del titolo dell'evento indicato in json_params['slave_event']
            "start_delay" : "70",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize_tickle"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "/invita-amici/{user_id}/{account_code}/",
            "json_params" : '{"slave_event": "friend_prize"}',
            "status" : "1",
        },
        event_code["friend_prize"] : {
            "ma_code" : event_code["friend_prize"],
            "description" : "Il bonus da mandare all'amico presentato",
            "prize_type" : "discount",
            "prize_value" : "20",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize"],
            "prize_call_to_action" : "/servizi/",
            "tickle_call_to_action" : "",
            "json_params" : '{"master_event": "refer_friend"}',
            "status" : "1",
        },
        event_code["get_review"] : {
            "ma_code" : event_code["get_review"],
            "description" : "Chiedo all'utente di lasciare una recensione (informazioni pubbliche)",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "98",
            "repeat_delay" : "168",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize_tickle"],
            "prize_call_to_action" : "/servizi/",
            "tickle_call_to_action" : "/lascia-una-recensione/{user_id}/{account_code}/",
            "status" : "1",
        },
        event_code["happy_birthday_prize"] : {
            "ma_code" : event_code["happy_birthday_prize"],
            "description" : "Bonus al compleanno",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "0",
            "repeat_delay" : "0",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["prize"],
            "prize_call_to_action" : "/servizi/",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        event_code["random_promo"] : {
            "ma_code" : event_code["random_promo"],
            "description" : "Premio con un testo random",
            "prize_type" : "discount",
            "prize_value" : "5",
            "start_delay" : "35",
            "repeat_delay" : "56",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["monthly_prize"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            #"json_params" : '{"current_random_promo_order": "-1"}',
            "status" : "1",
        },
        # tip mensili (mail senza codice)
        event_code["random_tip"] : {
            "ma_code" : event_code["random_tip"],
            "description" : "Mail di tip o info, non contiene codici sconto",
            "prize_type" : None,
            "prize_value" : None,
            "start_delay" : "28",
            "repeat_delay" : "28",
            "extra_text" : "",
            "ma_event_type" : ma_event_type["tip"],
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            #"json_params" : '{"current_random_tip_order": "-1"}',
            "status" : "1",
        },
        # TODO: mancano le promozioni basate sul tempo
    }

    feedback_quality_code = {
        "excellent" : {
            "quality_code" : "excellent",
            "quality_level" : "5",
            "quality_label" : "Eccellente",
        },
        "very_good" : {
            "quality_code" : "very_good",
            "quality_level" : "4",
            "quality_label" : "Molto buono",
        },
        "average" : {
            "quality_code" : "average",
            "quality_level" : "3",
            "quality_label" : "Nella media",
        },
        "low" : {
            "quality_code" : "low",
            "quality_level" : "2",
            "quality_label" : "Scarso",
        },
        "very_bad" : {
            "quality_code" : "very_bad",
            "quality_level" : "1",
            "quality_label" : "Pessimo",
        },
    }
