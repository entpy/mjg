# -*- coding: utf-8 -*-

# common utils object
from mkauto_app.models import *
from mkauto_app.consts import mkauto_consts
from promotion_app.models import *
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CommonUtils(object):

    CODE_TYPE_MKAUTO = "mkauto"
    CODE_TYPE_CAMPAIGN = "campaign"

    def identify_code_type(self, code):
        """Function to identify code type (mkauto, promo, ...) about code length"""

        return_var = False

        if len(code) == 8:
            return_var = self.CODE_TYPE_MKAUTO
        elif len(code) == 10:
            return_var = self.CODE_TYPE_CAMPAIGN

        return return_var

    # TODO
    def get_code_info(self, code):
        """Function to retrieve all info about a code"""

        return_var = {}

        if self.identify_code_type(code=code) == self.CODE_TYPE_MKAUTO:
            # è un codice della mkauto
            ma_event_code_obj = MaEventCode()
            ma_event_obj = MaEvent()
            ma_event_code_instance = ma_event_code_obj.get_by_code(code=code)
            # prelevo la stringa del premio
            
            code_content = ma_event_obj.get_event_generic_prize_str(ma_code=mkauto_consts.event_code[ma_event_code_instance.ma_event.ma_code])
            return_var["code"] = code
            return_var["content"] = "<b>" + str(code_content) + "</b>"
        elif self.identify_code_type(code=code) == self.CODE_TYPE_CAMPAIGN:
            # TODO
            # è un codice campagna
            campaign_obj = Campaign()
            campaign_order_obj = CampaignOrder()
            campaign_order_instance = campaign_order_obj.get_campaign_order_by_code(code=code)
            if campaign_order_instance:
                campaign_info_dict = campaign_obj.get_campaign_info_dict(campaign_order_instance.campaign_id)
                return_var["code"] = code
                return_var["content"] = "coupon di una campagna (vedi qui sotto i dettagli)<br /><br />Titolo campagna: " + str(campaign_info_dict["camp_title"]) + "<br />Costava: €" + str(campaign_info_dict["was_price_display"]) + "<br />Sconto: " + str(campaign_info_dict["discount_display"]) + "%<br /><b>Prezzo finale: €" + str(campaign_info_dict["final_price_display"]) + "</b>"

        return return_var

    def check_code_exists(self, code):
        """Function to check if a code exists"""

        return_var = False

        if self.identify_code_type(code=code) == self.CODE_TYPE_MKAUTO:
            ma_event_code_obj = MaEventCode()
            if ma_event_code_obj.check_event_code_exists(code=code):
                # codice esistente
                return_var = True
        elif self.identify_code_type(code=code) == self.CODE_TYPE_CAMPAIGN:
            campaign_order_obj = CampaignOrder()
            campaign_order_instance = campaign_order_obj.get_campaign_order_by_code(code=code)
            if campaign_order_instance:
                # codice esistente
                return_var = True

        return return_var

    def check_code_used(self, code):
        """Function to check if a code was marked as used"""

        return_var = False

        if self.identify_code_type(code=code) == self.CODE_TYPE_MKAUTO:
            ma_event_code_obj = MaEventCode()
            ma_event_code_instance = ma_event_code_obj.get_by_code(code=code)
            if ma_event_code_instance.status == 2:
                # codice già utilizzato
                return_var = True
        elif self.identify_code_type(code=code) == self.CODE_TYPE_CAMPAIGN:
            campaign_order_obj = CampaignOrder()
            campaign_order_instance = campaign_order_obj.get_campaign_order_by_code(code=code)
            if campaign_order_instance.status == 2:
                # codice già utilizzato
                return_var = True

        return return_var

    def mark_code_as_used(self, code):
        """Function to mark a code as used"""

        return_var = False

        if self.identify_code_type(code=code) == self.CODE_TYPE_MKAUTO:
            ma_event_code_obj = MaEventCode()
            ma_event_code_instance = ma_event_code_obj.get_by_code(code=code)
            ma_event_code_instance.status = 2
            ma_event_code_instance.save()
            return_var = True

            # se si tratta di un codice refer_friend mando il bonus a chi ha presentato l'amico
            # se il codice è di tipo "friend_prize"
            if ma_event_code_instance.ma_event.ma_code == mkauto_consts.event_code["friend_prize"]:
                # premio il cliente che ha proposto l'amico, ma prima devo capire chi l'ha proposto
                friend_code_obj = FriendCode()
                friend_code_instance = friend_code_obj.get_by_ma_event_code(ma_event_code_instance=ma_event_code_instance)

                # prelevo l'id dell'utente da premiare
                master_account_id = friend_code_instance.master_account_code.user.id

                friend_code_instance.status = True
                friend_code_instance.save()

                logger.debug("### mark_code_as_used")
                logger.debug("master_account_id: " + str(master_account_id))

                # invio il bonus
                ma_event_obj = MaEvent()
                ma_event_obj.make_event(user_id=master_account_id, ma_code=mkauto_consts.event_code["refer_friend"], strings_ma_code=mkauto_consts.event_code["refer_friend"], ma_code_dictionary=None, force_prize=True, skip_log_check=True)
        elif self.identify_code_type(code=code) == self.CODE_TYPE_CAMPAIGN:
            campaign_order_obj = CampaignOrder()
            campaign_order_instance = campaign_order_obj.get_campaign_order_by_code(code=code)
            if campaign_order_instance:
                campaign_order_instance.status = 2
                campaign_order_instance.save()
                return_var = True

        return return_var
