# -*- coding: utf-8 -*-

from django.core.mail import send_mail, EmailMultiAlternatives
from anymail.message import AnymailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings
from mjg_site.consts import project_constants
from itertools import chain
import logging, json, sys, copy

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_email_logo(logo_width=180):
    """Function to print email logo (header or footer)"""

    return_var = ""
    return_var += """
        <table style="max-width:600px;" class="wrapperWebview" cellspacing="0" cellpadding="0" border="0" width="100%">
                <tbody>
                        <tr>
                                <td valign="top" align="center">
                                        <!-- Content Table Open // -->
                                        <table cellspacing="0" cellpadding="0" border="0" width="100%">
                                                <tbody>
                                                        <tr>
                                                        <td style="padding-top:25px;padding-bottom:25px;" class="emailLogo" valign="middle" align="center">
                                                        <!-- Logo and Link // -->
                                                        <a href='""" + str(settings.SITE_URL) + """'>
                                                        <img class="emailMainLogo" src='""" + str(settings.SITE_URL) + """/static/website/img/email_logo.png' alt="MotorJab Garage" style="width:""" + str(logo_width) + """px; max-width:""" + str(logo_width) + """px!important;height:auto; display:block;" border="0" width='""" + str(logo_width) + """px'>
                                                        </a>
                                                        </td>
                                                        </tr>
                                                </tbody>
                                        </table>
                                        <!-- Content Table Close // -->
                                </td>
                        </tr>
                </tbody>
        </table>
    """

    return return_var

class CustomEmailTemplate():

    # the email inner blocks
    base_url = settings.SITE_URL

    # available email name (utilizzare quello chiamato 'customer_email')
    available_email_name = {
	'mkauto_email' : { # email della mkauto
	    'email_from' : settings.MKAUTO_EMAIL_ADDRESS,
	    'email_to' : 'user_email',
            'email_fields' : {
                "main_title_block" : "",
                "main_content_block" : "",
                "main_image_block" : "",
                "coupon_code_block" : "",
                "plain_main_title_block" : "",
                "plain_main_content_block" : "",
                "plain_coupon_code_block" : "",
                "call_to_action_block" : "",
                "plain_call_to_action_label" : "",
                "plain_call_to_action_url" : "",
                "user_profile_url" : "",
                "email_unsubscribe_url" : "",
                "unsubscribe_block" : "",
                "email_header_image_block" : mark_safe(get_email_logo(logo_width=180)), # per l'immagine presente nell'header
                # per la campagna {{{
                "email_footer_image_block" : "",
                "campaign_price_block" : "",
                "campaign_expiring_block" : "",
                # }}}
                "base_url" : settings.SITE_URL,
            }
	},
	'customer_email' : { # email della mkauto
	    'email_from' : settings.MKAUTO_EMAIL_ADDRESS,
	    'email_to' : 'user_email',
            'email_fields' : {
                "main_title_block" : "",
                "main_content_block" : "",
                "main_image_block" : "",
                "coupon_code_block" : "",
                "plain_main_title_block" : "",
                "plain_main_content_block" : "",
                "plain_coupon_code_block" : "",
                "call_to_action_block" : "",
                "plain_call_to_action_label" : "",
                "plain_call_to_action_url" : "",
                "user_profile_url" : "",
                "email_unsubscribe_url" : "",
                "unsubscribe_block" : "",
                "email_header_image_block" : "",
                "email_footer_image_block" : mark_safe(get_email_logo(logo_width=100)), # per l'immagine presente nel footer
                # per la campagna {{{
                "campaign_price_block" : "",
                "campaign_expiring_block" : "",
                # }}}
                "base_url" : settings.SITE_URL,
            }
	},
	'system_manage_email' : { # email di sistema
	    'email_from' : settings.DEVELOPER_EMAIL_ADDRESS,
	    'email_to' : 'info_email',
            'subject_prefix' : settings.SITE_NAME + " Admin - ",
            'email_fields' : {
                "main_title_block" : "",
                "main_content_block" : "",
                "plain_main_title_block" : "",
                "plain_main_content_block" : "",
                "base_url" : settings.SITE_URL,
            }
	},
	'blank_email' : { # blank email
	    'email_from' : settings.ADMIN_EMAIL_ADDRESS,
	    'email_to' : 'info_email',
            'subject_prefix' : settings.SITE_NAME + " - ",
            'email_fields' : {
                "main_content_block" : "",
                "plain_main_title_block" : "",
                "base_url" : settings.SITE_URL,
            }
	},
   }

    # email template directory (app name)
    template_dir = "email_app/"

    # list of email template available
    template_type = {
	"default": "default_template",
	"admin": "admin_template",
	"blank": "blank_template",
	# "user": "user_template",
    }

    def __init__(self, email_name, email_context, recipient_list=[], email_from=False, template_type="default", reply_to=False):

        # msg id
        msg_id = None
        # the email name, es. recover_password_email
        self.email_name = None

        # the email data, es. email and password in recover password email
        self.email_context = {}

        self.email_html_blocks = {}

        # email subject
        self.email_subject = None

        # email template name
        self.template_name = None

        self.email_from = False

        self.email_to = False

        self.reply_to = [settings.INFO_EMAIL_ADDRESS,]
        if reply_to:
            self.reply_to = [str(reply_to),]

        if email_name in chain(self.available_email_name):
	    # setting email from
	    self.set_email_from_address(email_name=email_name, email_from_forced=email_from)
	    # setting email to
	    self.set_email_to_address(email_name=email_name, user_email=recipient_list)

            # setting email name and context
            self.email_name = email_name
            self.email_context = email_context

            # setting template name, this override default template name
            # self.set_template_name(template_type=template_type)
            self.template_name = self.template_type.get(template_type, "default")

            # build email blocks
            self.build_email_template()

            # set email subject
            self.email_subject = self.email_context.get("subject")

            if self.available_email_name.get(email_name, {}).get("subject_prefix", ""):
                self.email_subject = str(self.available_email_name.get(email_name, {}).get("subject_prefix", "")) + self.email_subject

            # perform email sending
            self.msg_id = self.send_mail()

    def set_email_from_address(self, email_name, email_from_forced=False):
	"""Function to set email to address"""
	if email_from_forced:
	    # forzo il mittente della mail, senza tenere conto di quello specificato in 'self.available_email_name'
	    self.email_from = email_from_forced
	else:
            # se nel tipo di mail ho specificato un mittente utilizzo quello, altrimenti prelevo il default.
            # il from generalmente è la mail info (controllare nel file settings)
	    self.email_from = self.available_email_name[email_name].get('email_from', settings.DEFAULT_FROM_EMAIL)

	return True

    def set_email_to_address(self, email_name, user_email=[]):
	"""Function to set email from address"""
	email_to_type = self.available_email_name[email_name].get('email_to')
	if email_to_type == 'user_email':
	    # take user email
	    self.email_to = user_email
	elif email_to_type == 'info_email':
	    self.email_to = [settings.INFO_EMAIL_ADDRESS,]

	return True

    def build_dear_block(self):
	"""Function to build dear block"""
	return_var = "Caro utente,"
	first_name = self.email_context.get("first_name")
        """
	last_name = self.email_context.get("last_name")
	if last_name:
	    last_name = " " + last_name
        """

	if first_name:
	    # return_var = "Caro/a " + str(first_name)+str(last_name)+"," Dear First Name Last name,
	    return_var = str(first_name) + "," # Dear First Name, <- now use this

	return return_var

    def get_call_to_action_template(self, href, label, title=None):
	"""Function to retrieve call to action template"""
        title_html_block = ""
        cta_html_block = ""

        # se presente creo il blocco con il titolo della call to action
        if title:
            title_html_block = """
                <tr>
                    <td style="padding-bottom:10px;padding-left:15px;padding-right:15px;" class="callToActionTitle" valign="top" align="center">
                        <p class="text fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:18px;font-weight:bold;font-style:normal;letter-spacing:normal;line-height:35px;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(title) + """</p>
                    </td>
                </tr>
            """

        if href and label:
            cta_html_block = """
                <tr>
                    <td style="padding-bottom:50px;padding-left:15px;padding-right:15px;" class="callToActionButton" valign="top" align="center">
                        <div>
                            <!--[if mso]>
                                <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href='""" +  str(href) + """' style="height:40px;v-text-anchor:middle;width:200px;" arcsize="10%" stroke="f" fillcolor="#22c34b">
                                <w:anchorlock/>
                                <center>
                            <![endif]-->
                            <a href='""" +  str(href) + """' style="background-color:#22c34b;border-radius:4px;color:#ffffff;display:inline-block;font-family:'sans-serif', Helvetica, Arial;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;">""" + str(label) + """</a>
                            <!--[if mso]>
                                </center>
                                </v:roundrect>
                            <![endif]-->
                        </div>
                    </td>
                </tr>
            """

	return title_html_block + cta_html_block

    """
    def set_template_name(self, template_type=None):
        ""Function to set a template name starting from template type""
        self.template_name = self.template_type.get(template_type, "default_template")

        return True
    """

    def get_html_template(self):
        """Function to create html template"""
        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.html', self.email_html_blocks)

        return return_var

    def get_plain_template(self):
        """Function to create plain text template"""
        return_var = False
        if self.template_name:
            return_var = render_to_string(self.template_dir + self.template_name + '.txt', self.email_html_blocks)

        logger.info("@@@")
        logger.info(return_var)
        logger.info("@@@")
        return return_var

    def get_image_block(self, image_url, email_name="mkauto_email"):
        """Function to create email image block"""
        return_var = ""
        if email_name == "mkauto_email":
            return_var = """
                <tr>
                        <td style="padding-bottom:50px;padding-left:15px;padding-right:15px;" class="imgHero" valign="top" align="center">
                                <!-- Hero Image // -->
                                <img class="emailMainImage" src='""" + str(image_url) + """' alt="Image" style="display: block; height: auto; max-width: 350px; width: 100%;" border="0">
                        </td>
                </tr>
            """

        return return_var

    def get_unsubscribe_block(self, user_profile_url, email_unsubscribe_url):
        """Function to create email unsubscribe block"""
        return_var = ""
        if user_profile_url and email_unsubscribe_url:
            return_var = """
                <tr>
                        <td style="padding:0px 10px 10px;" class="footerEmailInfo" valign="top" align="center">
                                <!-- Information of NewsLetter (Subscribe Info)// -->
                                <p class="text fallback-text" style="color:#777777;font-family:Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;font-style:normal;letter-spacing:normal;line-height:20px;text-transform:none;text-align:center;padding:0;margin:0;">
                                        Puoi disiscriverti o modificare le tue preferenze in qualsiasi momento cliccando i link sotto.<br><a style="color:#777777;font-family:Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;font-style:normal;letter-spacing:normal;line-height:20px;text-decoration:underline;" href='""" + str(user_profile_url) + """'>modifica preferenze</a> o <a style="color:#777777;font-family:Helvetica, Arial, sans-serif;font-size:12px;font-weight:400;font-style:normal;letter-spacing:normal;line-height:20px;text-decoration:underline;" href='""" + str(email_unsubscribe_url) + """'>disiscriviti</a>.
                                </p>
                        </td>
                </tr>
            """

        return return_var

    def get_coupon_code_block(self, coupon_code, email_name="mkauto_email"):
        """Function to create email coupon code block"""
        return_var = ""
        if email_name == "mkauto_email":
            return_var += """
                <tr>
                        <td style="padding-bottom:25px;padding-left:20px;padding-right:20px;" class="subTitle" valign="top" align="center">
                                <!-- Sub Title Text // -->
                                <h4 class="text emailCouponInfo fallback-text" style="color:#999999;font-family:'sans-serif', Helvetica, Arial;font-size:16px;font-weight:400;font-style:normal;letter-spacing:normal;line-height:24px;text-transform:none;text-align:center;padding:0;margin:0;">Presentaci il codice sotto in sede per ottenere il bonus:</h4>
                        </td>
                </tr>
                <tr>
                        <td style="padding-left:20px;padding-right:20px;" class="containtTable ui-sortable" valign="top" align="center">
                                <table class="tableMediumTitle" cellspacing="0" cellpadding="0" border="0" width="100%">
                                        <tbody>
                                                <tr>
                                                        <td style="padding-bottom:30px;" class="mediumTitle" valign="top" align="center">
                                                                <!-- Medium Title Text // -->
                                                                <p class="text emailCouponCode fallback-text" style="color:#F92D41;font-family:'sans-serif', Helvetica, Arial;font-size:34px;font-weight:500;font-style:normal;letter-spacing:normal;line-height:24px;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(coupon_code) + """</p>
                                                        </td>
                                                </tr>
                                        </tbody>
                                </table>
                        </td>
                </tr>
            """

        return return_var

    def get_campaign_price_block(self, was_price, final_price, discount, saving):
        """Function to retrieve campaign email price block"""

        currency="&euro;"
        return_var = ""
        if was_price and final_price and discount and saving:
            return_var += """
                <tr>
                        <td style="padding-bottom:25px;" class="description" valign="top" align="center">
                                <table style="width: 100%;">
                                        <tr><td style="text-align: center;line-height: normal;"><span class="text emailCampaignPriceTitle fallback-text" style="color:#008b99;font-family:'sans-serif', Helvetica, Arial;font-size:16px;font-weight:bold;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">Prezzo</span></td></tr>
                                        <tr><td style="text-align: center;line-height: normal;"><span class="text emailCampaignPriceCurrency fallback-text" style="color:#008b99;font-family:'sans-serif', Helvetica, Arial;font-size:35px;font-weight:100;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;margin-right: 5px;">""" + str(currency) + """</span><span class="text emailCampaignPriceValue fallback-text" style="color:#008b99;font-family:'sans-serif', Helvetica, Arial;font-size:47px;font-weight:bold;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(final_price) + """</span></td></tr>
                                </table>
                        </td>
                </tr>
                <tr>
                        <td style="padding-bottom:20px;" class="description" valign="top" align="center">
                                <table style="width: 100%; border-top: 1px solid #cccaca; border-bottom: 1px solid #cccaca;">
                                        <tr>
                                                <td style="text-align: center; padding-top: 10px;line-height: normal;"><span class="text emailCampaignDiscountTitle fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:13px;font-weight:300;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">Costava</span></td>
                                                <td style="text-align: center; padding-top: 10px;line-height: normal;"><span class="text emailCampaignDiscountTitle fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:13px;font-weight:300;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">Sconto</span></td>
                                                <td style="text-align: center; padding-top: 10px;line-height: normal;"><span class="text emailCampaignDiscountTitle fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:13px;font-weight:300;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">Risparmi</span></td>
                                        </tr>
                                        <tr>
                                                <td style="text-align: center; padding-bottom: 10px;line-height: normal;"><span class="text emailCampaignDiscounturrency fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:18px;font-weight:100;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;margin-right: 5px;">""" + str(currency) + """</span><span class="text emailCampaignDiscountValue fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:25px;font-weight:100;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(was_price) + """</span></td>
                                                <td style="text-align: center; padding-bottom: 10px;line-height: normal;"><span class="text emailCampaignDiscountValue fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:25px;font-weight:400;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(discount) + """%</span></td>
                                                <td style="text-align: center; padding-bottom: 10px;line-height: normal;"><span class="text emailCampaignDiscounturrency fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:18px;font-weight:100;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;margin-right: 5px;">""" + str(currency) + """</span><span class="text emailCampaignDiscountValue fallback-text" style="color:#333;font-family:'sans-serif', Helvetica, Arial;font-size:25px;font-weight:400;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(saving) + """</span></td>
                                        </tr>
                                </table>
                        </td>
                </tr>
            """

        return return_var

    def get_campaign_expiring_block(self, expiring_str):
        """Function to retrieve campaign email expiring block"""

        return_var = ""
        if expiring_str:
            return_var += """
                <tr>
                        <td style="padding-bottom:50px;" class="description" valign="top" align="center">
                                <table style="width: 100%;">
                                        <tr>
                                                <td style="text-align: center; padding-top: 10px;line-height: normal;"><span class="text emailCampaignDiscountTitle fallback-text" style="color:#ff0505;font-family:'sans-serif', Helvetica, Arial;font-size:13px;font-weight:300;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">Affrettati, scade tra</span></td>
                                        </tr>
                                        <tr>
                                                <td style="text-align: center; padding-bottom: 10px;line-height: normal;"><span class="text emailCampaignDiscountValue fallback-text" style="color:#ff0505;font-family:'sans-serif', Helvetica, Arial;font-size:25px;font-weight:100;font-style:normal;letter-spacing:normal;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(expiring_str) + """</span></td>
                                        </tr>
                                </table>
                        </td>
                </tr>
            """

        return return_var

    def build_email_template(self):
        """Function to create the email template before sending"""
        return_var = False
	if self.email_name in chain(self.available_email_name):
            if self.email_name == "mkauto_email":
                """
                costruisco la mail per la mkauto
                Context vars (* required):
                ->    ['title *',
                       'content *',
                       'image_url',
                       'coupon_code',
                       'coupon_code_extra_text',
                       'call_to_action_title',
                       'call_to_action_label',
                       'call_to_action_url',
                      ]
		come prelevare una variabile -> str(self.email_context.get("email"))

                1) inizializzo i blocchi della mail
                2) creo i blocchi per la versione html
                3) creo i blocchi per la versione plain text
                """
                # 1) inizializzo tutti i blocchi della mail (è fondamentale l'utilizzo di deepcopy)
                self.email_html_blocks = copy.deepcopy(self.available_email_name[self.email_name]["email_fields"])

                # 2) html version {{{
                self.email_html_blocks["main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["main_content_block"] = mark_safe(self.email_context.get("content"))

                if self.email_context.get("coupon_code_extra_text"):
                    self.email_html_blocks["main_content_block"] += mark_safe(self.email_context.get("coupon_code_extra_text"))

                # se presente il codice di un'immagine inserisco il blocco con l'immagine
                if self.email_context.get("image_url"):
                    self.email_html_blocks["main_image_block"] = mark_safe(self.get_image_block(image_url=self.email_context.get("image_url")))

                # se presente il codice coupon inserisco il blocco con il codice coupon, con l'eventuale testo aggiuntivo
                if self.email_context.get("coupon_code"):
                    self.email_html_blocks["coupon_code_block"] = mark_safe(self.get_coupon_code_block(coupon_code=self.email_context.get("coupon_code")))
                # html version }}}

                # 3) plain text version {{{
                self.email_html_blocks["plain_main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["plain_main_content_block"] = mark_safe("\n" + self.email_context.get("content") + "\n")

                if self.email_context.get("coupon_code_extra_text"):
                    self.email_html_blocks["plain_main_content_block"] += mark_safe("\n" + self.email_context.get("coupon_code_extra_text"))

                # se presente il codice coupon inserisco il blocco con il codice coupon, con l'eventuale testo aggiuntivo
                self.email_html_blocks["plain_coupon_code_block"] = ""
                if self.email_context.get("coupon_code"):
                    # se presente un testo addizionale lo inserisco prima del codice
                    if self.email_context.get("coupon_code_extra_text"):
                        self.email_html_blocks["plain_coupon_code_block"] += mark_safe(self.email_context.get("coupon_code_extra_text")) + "\n"
                    self.email_html_blocks["plain_coupon_code_block"] += mark_safe(self.email_context.get("coupon_code"))
                # plain text version }}}

                # se presente una call to action, inseirsco un pulsante nella versione html e il link nella versione testuale
                if self.email_context.get("call_to_action_label") and self.email_context.get("call_to_action_url"):
                    call_to_action_url = self.base_url + str(self.email_context.get("call_to_action_url"))
                    self.email_html_blocks["call_to_action_block"] = mark_safe(self.get_call_to_action_template(href=call_to_action_url, label=self.email_context.get("call_to_action_label"), title=self.email_context.get("call_to_action_title")))
                    self.email_html_blocks["plain_call_to_action_label"] = "&nbsp;" + str(mark_safe(self.email_context.get("call_to_action_label"))) + "&nbsp;"
                    self.email_html_blocks["plain_call_to_action_url"] = mark_safe(call_to_action_url)

                # link di unsubscribe e profile editing
                if self.email_context.get("email_unsubscribe_url"):
                    self.email_html_blocks["email_unsubscribe_url"] = mark_safe(self.email_context.get("email_unsubscribe_url"))

                # creo il blocco di unsubscribe
                if self.email_context.get("user_profile_url") and self.email_context.get("email_unsubscribe_url"):
                    self.email_html_blocks["unsubscribe_block"] = mark_safe(self.get_unsubscribe_block(user_profile_url=self.email_context.get("user_profile_url"), email_unsubscribe_url=self.email_context.get("email_unsubscribe_url")))
                pass
            if self.email_name == "customer_email":
                """
                costruisco la mail per la mkauto
                Context vars (* required):
                ->    ['title *',
                       'content *',
                       'image_url',
                       'coupon_code',
                       'coupon_code_extra_text',
                       'call_to_action_title',
                       'call_to_action_label',
                       'call_to_action_url',
                      ]
		come prelevare una variabile -> str(self.email_context.get("email"))

                1) inizializzo i blocchi della mail
                2) creo i blocchi per la versione html
                3) creo i blocchi per la versione plain text
                """
                # 1) inizializzo tutti i blocchi della mail (è fondamentale l'utilizzo di deepcopy)
                self.email_html_blocks = copy.deepcopy(self.available_email_name[self.email_name]["email_fields"])

                # 2) html version {{{
                self.email_html_blocks["main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["main_content_block"] = mark_safe(self.email_context.get("content"))

                if self.email_context.get("coupon_code_extra_text") and self.email_context["coupon_code_extra_text"]:
                    self.email_html_blocks["main_content_block"] += mark_safe(self.email_context.get("coupon_code_extra_text"))

                # se presente il codice coupon inserisco il blocco con il codice coupon, con l'eventuale testo aggiuntivo
                if self.email_context.get("coupon_code") and self.email_context["coupon_code"]:
                    self.email_html_blocks["coupon_code_block"] = mark_safe(self.get_coupon_code_block(coupon_code=self.email_context.get("coupon_code")))

                # se presente il codice di un'immagine inserisco il blocco con l'immagine
                if self.email_context.get("image_url"):
                    self.email_html_blocks["main_image_block"] = mark_safe(self.get_image_block(image_url=self.email_context.get("image_url")))

                # TODO {{{
                # controllo se inserire il blocco dei prezzi
                if self.email_context.get("campaign_was_price") and self.email_context.get("campaign_final_price") and self.email_context.get("campaign_discount") and self.email_context.get("campaign_saving"):
                    if self.email_context["campaign_was_price"] and self.email_context["campaign_final_price"] and self.email_context["campaign_discount"] and self.email_context["campaign_saving"]:
                        self.email_html_blocks["campaign_price_block"] = mark_safe(self.get_campaign_price_block(was_price=self.email_context.get("campaign_was_price"), final_price=self.email_context.get("campaign_final_price"), discount=self.email_context.get("campaign_discount"), saving=self.email_context.get("campaign_saving")))

                # TODO
                # controllo se inserire il blocco con la scadenza
                if self.email_context.get("campaign_expiring") and self.email_context["campaign_expiring"]:
                    self.email_html_blocks["campaign_expiring_block"] = mark_safe(self.get_campaign_expiring_block(expiring_str=self.email_context.get("campaign_expiring")))
                # TODO }}}
                # html version }}}

                # 3) plain text version {{{
                self.email_html_blocks["plain_main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["plain_main_content_block"] = mark_safe("\n" + self.email_context.get("content") + "\n")

                # se presente il codice coupon inserisco il blocco con il codice coupon, con l'eventuale testo aggiuntivo
                self.email_html_blocks["plain_coupon_code_block"] = ""
                if self.email_context.get("coupon_code"):
                    # se presente un testo addizionale lo inserisco prima del codice
                    if self.email_context.get("coupon_code_extra_text"):
                        self.email_html_blocks["plain_coupon_code_block"] += mark_safe(self.email_context.get("coupon_code_extra_text")) + "\n"
                    self.email_html_blocks["plain_coupon_code_block"] += mark_safe(self.email_context.get("coupon_code"))
                # plain text version }}}

                # se presente una call to action, inseirsco un pulsante nella versione html e il link nella versione testuale
                if self.email_context.get("call_to_action_label") and self.email_context.get("call_to_action_url"):
                    call_to_action_url = self.base_url + str(self.email_context.get("call_to_action_url"))
                    self.email_html_blocks["call_to_action_block"] = mark_safe(self.get_call_to_action_template(href=call_to_action_url, label=self.email_context.get("call_to_action_label"), title=self.email_context.get("call_to_action_title")))
                    self.email_html_blocks["plain_call_to_action_label"] = "&nbsp;" + str(mark_safe(self.email_context.get("call_to_action_label"))) + "&nbsp;"
                    self.email_html_blocks["plain_call_to_action_url"] = mark_safe(call_to_action_url)

                # link di unsubscribe e profile editing
                if self.email_context.get("email_unsubscribe_url"):
                    self.email_html_blocks["email_unsubscribe_url"] = mark_safe(self.email_context.get("email_unsubscribe_url"))

                # creo il blocco di unsubscribe
                if self.email_context.get("user_profile_url") and self.email_context.get("email_unsubscribe_url"):
                    self.email_html_blocks["unsubscribe_block"] = mark_safe(self.get_unsubscribe_block(user_profile_url=self.email_context.get("user_profile_url"), email_unsubscribe_url=self.email_context.get("email_unsubscribe_url")))
                pass
            elif self.email_name == "system_manage_email":
                """
                costruisco la mail per gli admin
                Context vars (* required):
                ->    ['title *',
                       'content *',
                      ]
		come prelevare una variabile -> str(self.email_context.get("email"))
                """
                # 1) inizializzo tutti i blocchi della mail (è fondamentale l'utilizzo di deepcopy)
                self.email_html_blocks = copy.deepcopy(self.available_email_name[self.email_name]["email_fields"])

                # 2) html version {{{
                self.email_html_blocks["main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["main_content_block"] = mark_safe(self.email_context.get("content"))

                # 3) plain text version {{{
                self.email_html_blocks["plain_main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["plain_main_content_block"] = mark_safe("\n" + self.email_context.get("content") + "\n")
                pass
            elif self.email_name == "blank_email":
                """
                costruisco la mail per gli admin
                Context vars (* required):
                ->    ['title *',
                       'content *',
                      ]
		come prelevare una variabile -> str(self.email_context.get("email"))
                """
                # 1) inizializzo tutti i blocchi della mail (è fondamentale l'utilizzo di deepcopy)
                self.email_html_blocks = copy.deepcopy(self.available_email_name[self.email_name]["email_fields"])

                # 2) html version {{{
                self.email_html_blocks["main_content_block"] = mark_safe(self.email_context.get("content"))

                # 3) plain text version {{{
                self.email_html_blocks["plain_main_content_block"] = mark_safe("\n" + self.email_context.get("content") + "\n")
                pass

            return_var = True
        else:
            logger.error("mail name " + str(self.email_name) + " is not a valid email template")

        return return_var

    def send_mail(self):
        """Function to send email"""
	return_var = None
        send_status = None
	plain_text = self.get_plain_template()
	html_text = self.get_html_template()

        # send email
        text_content = plain_text
        html_content = html_text
        msg = AnymailMessage(subject=self.email_subject, body=text_content, from_email=self.email_from, to=self.email_to, reply_to=self.reply_to)
        msg.attach_alternative(html_content, "text/html")
        send_status = msg.send()
        status = msg.anymail_status  # available after sending
        return_var = status.message_id  # e.g., '<12345.67890@example.com>'

	"""
        logger.info("###START EMAIL HTML###")
        logger.info(html_text)
        logger.info("###END EMAIL HTML###")
	"""

        logger.info("email inviata a " + str(self.email_to) + " | stato invio: " + str(send_status) + " (1=ok) | msg_id: " + str(return_var))

        return return_var
