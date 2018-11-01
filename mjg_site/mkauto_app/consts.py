# -*- coding: utf-8 -*-

"""
In this module will be defined all strings about mkauto (subject, title and text)
"""
class mkauto_consts(object):
    event_code = {
        # promozioni automatiche su flusso dell'utente
        "welcome_prize" : "welcome_prize", # prize -> premio alla registrazione
        "get_birthday_date" : "get_birthday_date", # tickle -> premio per lasciare la data di nascita
        "happy_birthday_prize" : "happy_birthday_prize", # prize -> premio al compleanno
        "get_feedback" : "get_feedback", # tickle -> per lasciare un feedback
        "get_review" : "get_review", # tickle -> per lasciare una recensione
        "refer_friend" : "refer_friend", # tickle -> per proporre un amico
        # promozioni automatiche basate sul tempo
        "tires_promotion_summer" : "tires_promotion_summer", # cambio gomme per l'estate
        "tires_promotion_winter" : "tires_promotion_winter", # cambio gomme per l'inverno
        "services_promotion" : "services_promotion", # tagliando estivo stagionale
        "air_conditioning_promotion" : "air_conditioning_promotion", # ricarica climatizzatore
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
            "is_tickle" : "0",
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
        {
            "ma_code" : event_code["get_birthday_date"],
            "description" : "Lasciaci la data di nascita per ricevere un bonus",
            "prize_type" : "discount",
            "prize_value" : "15",
            "start_delay" : "30",
            "repeat_delay" : "0",
            "extra_text" : "",
            "is_tickle" : "1",
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
            "is_tickle" : "0",
            "prize_call_to_action" : "",
            "tickle_call_to_action" : "",
            "status" : "1",
        },
    ]
