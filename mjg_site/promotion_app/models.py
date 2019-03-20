# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mjg_site.consts import project_constants
import datetime, random, string, sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Campaign(models.Model):
    CAMPAIGN_TYPE = (
        (project_constants.CAMPAIGN_TYPE_PROMOTION, project_constants.CAMPAIGN_TYPE_PROMOTION),
        (project_constants.CAMPAIGN_TYPE_NEWSLETTER, project_constants.CAMPAIGN_TYPE_NEWSLETTER),
    )
    CAMPAIGN_STATUS = (
        (project_constants.CAMPAIGN_STATUS_IN_WORKING, project_constants.CAMPAIGN_STATUS[CAMPAIGN_STATUS_IN_WORKING]),
        (project_constants.CAMPAIGN_STATUS_SENDING, project_constants.CAMPAIGN_STATUS[CAMPAIGN_STATUS_SENDING]),
        (project_constants.CAMPAIGN_STATUS_SENT, project_constants.CAMPAIGN_STATUS[CAMPAIGN_STATUS_SENT]),
    )
    campaign_id = models.AutoField(primary_key=True)
    msg_subject = models.CharField(max_length=200, null=False, blank=False, verbose_name="Indica l'oggetto nel messaggio")
    msg_title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Indica il titolo nel messaggio")
    msg_text = models.TextField(False=True, blank=False, verbose_name="Indica il testo nel messaggio")
    was_price = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=15, verbose_name="Prezzo iniziale")
    final_price = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=15, verbose_name="Prezzo finale")
    discount = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=15)
    image = models.ImageField(blank=True, null=True,verbose_name="Immagine della promozione", upload_to=project_constants.CAMPAIGN_UPLOAD_DIR)
    campaign_type = models.CharField(max_length=30, null=False, blank=False, choices=CAMPAIGN_TYPE, verbose_name="Indica il tipo di campagna (Promozione|Newsletter)")
    status = models.IntegerField(default=1, choices=CAMPAIGN_STATUS, verbose_name="Indica lo stato della campagna (1=in lavorazione, 2=in fase di invio, 3=inviata)")
    expiring_date = models.DateTimeField(null=False, blank=False, verbose_name"Data di scadenza della promozione (scadenza minima=1 mese)")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'promotion_app'

    def __unicode__(self):
        return str(self.campaign_id)

class CampaignDest(models.Model):
    campaign_dest_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=25, null=False, blank=False, verbose_name="Il codice univoco generato per il destinatario")
    dest = models.CharField(max_length=50, null=False, blank=False, verbose_name="Dove inviare la promozione")
    channel = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name"Canale di destinazione (email/sms)")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'promotion_app'

    def __unicode__(self):
        return str(self.campaign_dest_id)

    # TODO
    def generate_dest_code(self, depth=0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

        if CampaignDest.objects.filter(code=random_code).exists():
            # than recall this function to generate a new ones
            if depth < 50:
                random_code = self.generate_dest_code(depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        else:
            # il codice non esiste in db pertano può essere utilizzato
            pass

        return random_code

class CampaignUserTemp(models.Model):
    campaign_user_temp_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dest = models.CharField(max_length=50, null=False, blank=False)
    channel = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name"Canale di destinazione")

    class Meta:
        app_label = 'promotion_app'

    def __unicode__(self):
        return str(self.campaign_user_temp_id)

class CampaignOrder(models.Model):
    campaign_order_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, null=False, blank=False, verbose_name="Il codice generato, quello evenetualmente da bruciare")
    status = models.IntegerField(null=False, blank=False, default=1, verbose_name="Indica se il codice è utilizzato o no (1=non utilizzato 2=utilizzato)")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'promotion_app'

    def __unicode__(self):
        return str(self.campaign_order_id)

    # TODO
    def generate_random_code(self, depth=0):
        """
        Generating a random promo code, if the generated code already
        exists, than recursively call this function to generate a new ones.
        Max recursion depth: 50
        """

        # generating a random code
        random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        if CampaignOrder.objects.filter(code=random_code).exists():
            # than recall this function to generate a new ones
            if depth < 50:
                random_code = self.generate_random_code(depth+1)
            else:
                logger.error("ATTENZIONE: non sono riuscito a generare un nuovo codice | depth level: " + str(depth))
                random_code = "PROMOCODE1"
        else:
            # il codice non esiste in db pertano può essere utilizzato
            pass

        return random_code
