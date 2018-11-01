# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings
from mjg_site.consts import project_constants
from itertools import chain
import logging, json, sys

# force utf8 read data
reload(sys);
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CustomEmailTemplate():

    # the email name, es. recover_password_email
    email_name = None

    # the email data, es. email and password in recover password email
    email_context = {}

    # the email inner blocks
    base_url = settings.SITE_URL
    email_html_blocks = {}

    # email subject
    email_subject = None

    # email template name
    template_name = None

    # available email name
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
            }
	},
	'system_manage_email' : { # email di sistema
	    'email_from' : settings.DEVELOPER_EMAIL_ADDRESS,
	    'email_to' : 'info_email',
	},
   }

    # email template directory (app name)
    template_dir = "email_app/"

    # list of email template available
    template_type = {
	"default": "default_template",
	# "user": "user_template",
	# "admin": "admin_template",
    }

    email_from = False,

    email_to = False,

    def __init__(self, email_name, email_context, recipient_list=[], email_from=False, template_type="default"):

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

            # perform email sending
            self.send_mail()

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

    def get_call_to_action_template(self, href=None, label=None):
	"""Function to retrieve call to action template"""
	return_var = False

	if href and label:
	    return_var = '<a style="display: inline-block;text-decoration: none;-webkit-text-size-adjust: none;mso-hide: all;text-align: center;font-family: Verdana,Geneva,sans-serif;-webkit-border-radius: 4px;-moz-border-radius: 4px;border-radius: 4px;border-top: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-left: 0px solid transparent;color: #ffffff !important;padding: 5px 20px 5px 20px;vertical-align: middle" href="' + str(href) + '" target="_blank">'
	    return_var += '<!--[if gte mso 9]>&nbsp;<![endif]-->'
	    return_var += '<div style="text-align: center;font-family: inherit;font-size: 16px;line-height: 32px;color: #ffffff;min-width: 220px">' + str(label) + '</div>'
	    return_var += '<!--[if gte mso 9]>&nbsp;<![endif]-->'
	    return_var += '</a>'

	return return_var

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

    def get_coupon_code_block(self, coupon_code, email_name="mkauto_email", coupon_code_extra_text=None):
        """Function to create email coupon code block"""
        return_var = ""
        if email_name == "mkauto_email":
            if coupon_code_extra_text:
                return_var += """
                    <tr>
                            <td style="padding-bottom:25px;padding-left:20px;padding-right:20px;" class="subTitle" valign="top" align="center">
                                    <!-- Sub Title Text // -->
                                    <h4 class="text emailCouponInfo fallback-text" style="color:#999999;font-family:'sans-serif', Helvetica, Arial;font-size:16px;font-weight:400;font-style:normal;letter-spacing:normal;line-height:24px;text-transform:none;text-align:center;padding:0;margin:0;">""" + str(coupon_code_extra_text) + """</h4>
                            </td>
                    </tr>
                """
            return_var += """
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

    def build_email_template(self):
        """Function to create the email template before sending"""
        return_var = False
        # reset di tutti i campi da sostituire
        # XXX: potrebbe essere superfluo
        """
        self.email_html_blocks = {
            "main_title_block": "",
            "main_content_block": "",
            "main_image_block": "",
            "coupon_code_block": "",
            "plain_main_title_block": "",
            "plain_main_content_block": "",
            "plain_coupon_code_block": "",
        }
        """
	if self.email_name in chain(self.available_email_name):
            if self.email_name == "mkauto_email":
                """
                costruisco la mail per la mkauto
                Context vars (* required):
                ->    ['title *', 'content *', 'image_code', 'coupon_code', 'coupon_code_extra_text',]
		come prelevare una variabile -> str(self.email_context.get("email"))

                1) inizializzo i blocchi della mail
                2) creo i blocchi per la versione html
                3) creo i blocchi per la versione plain text
                """
                # 1) inizializzo tutti i blocchi della mail
                self.email_html_blocks = self.available_email_name[self.email_name]["email_fields"]

                # 2) html version {{{
                self.email_html_blocks["main_title_block"] = mark_safe(self.email_context.get("title"))
                self.email_html_blocks["main_content_block"] = mark_safe(self.email_context.get("content"))

                # se presente il codice di un'immagine inserisco il blocco con l'immagine
                if self.email_context.get("image_code"):
                    self.email_html_blocks["main_image_block"] = mark_safe(self.get_image_block(image_url=self.base_url + "/static/website/img/mkauto_images/" + self.email_context.get("image_code") + ".png"))

                # se presente il codice coupon inserisco il blocco con il codice coupon, con l'eventuale testo aggiuntivo
                if self.email_context.get("coupon_code"):
                    self.email_html_blocks["coupon_code_block"] = mark_safe(self.get_coupon_code_block(coupon_code=self.email_context.get("coupon_code"), coupon_code_extra_text=self.email_context.get("coupon_code_extra_text")))
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

                # TODO
                # prevedere una call to action al fondo del template
                # self.email_html_blocks["html_call_to_action_block"] = self.get_call_to_action_template(href=self.base_url + "/profilo/zona-proibita/", label="Accedi ora")

                pass

            return_var = True
        else:
            logger.error("mail name " + str(self.email_name) + " is not a valid email template")

        return return_var

    def send_mail(self):
        """Function to send email"""
	return_var = None
	plain_text = self.get_plain_template()
	html_text = self.get_html_template()

        # send email
        return_var = send_mail(
            subject=self.email_subject,
            message=plain_text,
            from_email=self.email_from,
            recipient_list=self.email_to,
            html_message=html_text,
        )
        logger.info("email inviata a " + str(self.email_to) + " | stato invio: " + str(return_var) + " (1=ok)")
        """
        send_debug_admin_email = True

	# sending email to admin
	# logger.info("@@@admin email: " + str(settings.ADMINS[0][1]))
	if send_debug_admin_email:
	    return_var = send_mail(
		subject="<Django email system>" + self.email_subject,
		message=plain_text,
		from_email=self.email_from,
		recipient_list=[settings.DEVELOPER_EMAIL_ADDRESS,],
		html_message=html_text,
	    )
        """

	#logger.info("###invio la mail all'admin:  " + str(mail_admins_status) + "###")

        return return_var
