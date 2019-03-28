# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mjg_site.consts import project_constants
from mjg_site.CustomImagePIL import CustomImagePIL
import datetime, random, string, sys, logging

# force utf8 read data
reload(sys)
sys.setdefaultencoding("utf8")

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CampaignImage(models.Model):
    IMAGE_SIZE = (
        ("m", "m"),
        ("l", "l"),
    )
    campaign_image_id = models.AutoField(primary_key=True)
    image = models.ImageField(blank=False, null=False,verbose_name="Immagine della promozione", upload_to=project_constants.CAMPAIGN_UPLOAD_DIR)
    size = models.CharField(max_length=1, null=False, blank=False, choices=IMAGE_SIZE, verbose_name="Indica la dimensione dell'immagine")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'promotion_app'

    def __unicode__(self):
        return str(self.campaign_image_id)

    def save(self, *args, **kwargs):
        """Overriding save method to handle uploaded image"""

        # saving model
        super(CampaignImage, self).save(*args, **kwargs) # Call the "real" save() method.

        # resize image
        if self.image:
            if self.size == "m":
                custom_image_PIL_obj = CustomImagePIL(file_path=str(self.image.path), image_raw=None, box_width=500, box_height=500)
                custom_image_PIL_obj.resize_image(filename=self.image.path)
            elif self.size == "l":
                custom_image_PIL_obj = CustomImagePIL(file_path=str(self.image.path), image_raw=None, box_width=800, box_height=800)
                custom_image_PIL_obj.resize_image(filename=self.image.path)

class Campaign(models.Model):
    CAMPAIGN_TYPE = (
        (project_constants.CAMPAIGN_TYPE_PROMOTION, project_constants.CAMPAIGN_TYPE_PROMOTION),
        (project_constants.CAMPAIGN_TYPE_NEWSLETTER, project_constants.CAMPAIGN_TYPE_NEWSLETTER),
    )
    campaign_id = models.AutoField(primary_key=True)
    camp_title = models.CharField(max_length=200, null=False, blank=False, verbose_name="Indica il titolo della campagna")
    camp_description = models.TextField(null=False, blank=False, verbose_name="Indica la descrizione della campagna")
    msg_subject = models.CharField(max_length=200, null=False, blank=False, verbose_name="Indica l'oggetto nel messaggio")
    msg_text = models.TextField(null=False, blank=False, verbose_name="Indica il testo nel messaggio")
    was_price = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=15, verbose_name="Prezzo iniziale")
    final_price = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=15, verbose_name="Prezzo finale")
    discount = models.DecimalField(null=True, blank=True, max_digits=18, decimal_places=15)
    small_image = models.ForeignKey(CampaignImage, related_name="CampaignImage_small", blank=True, null=True, on_delete=models.SET_NULL)
    large_image = models.ForeignKey(CampaignImage, related_name="CampaignImage_large", blank=True, null=True, on_delete=models.SET_NULL)
    campaign_type = models.CharField(max_length=30, null=False, blank=False, choices=CAMPAIGN_TYPE, verbose_name="Indica il tipo di campagna (Promozione|Newsletter)")
    channel = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name="Canale di destinazione (email/sms)")
    status = models.IntegerField(default=1, choices=project_constants.CAMPAIGN_STATUS, verbose_name="Indica lo stato della campagna (1=in lavorazione, 2=in fase di invio, 3=inviata)")
    expiring_date = models.DateField(null=True, blank=False, verbose_name="Data di scadenza della promozione (scadenza minima=1 mese a partire da creazione promo)")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'promotion_app'
        indexes = [
            models.Index(fields=['campaign_type',]),
            models.Index(fields=['channel',]),
            models.Index(fields=['status',]),
            models.Index(fields=['expiring_date',]),
        ]

    def __unicode__(self):
        return str(self.campaign_id)

    def create_update_campaign(self, data_dict = {}, campaign_id=None):
        """Function to create or update a campaign"""

        campaign_obj = Campaign()

        if campaign_id:
            try:
                campaign_obj = Campaign.objects.get(campaign_id=campaign_id)
            except Campaign.DoesNotExist:
                # l'oggetto non esiste, notifico l'errore
                logger.error("errore in create_update_campaign, oggetto non esistente")
                raise 

        # salvo/aggiorno i dati della campagna
        if "camp_title" in data_dict:
            campaign_obj.camp_title = data_dict["camp_title"]
        if "camp_description" in data_dict:
            campaign_obj.camp_description = data_dict["camp_description"]
        if "msg_subject" in data_dict:
            campaign_obj.msg_subject = data_dict["msg_subject"]
        if "msg_text" in data_dict:
            campaign_obj.msg_text = data_dict["msg_text"]
        if "was_price" in data_dict:
            campaign_obj.was_price = data_dict["was_price"]
        if "final_price" in data_dict:
            campaign_obj.final_price = data_dict["final_price"]
        if "discount" in data_dict:
            campaign_obj.discount = data_dict["discount"]
        if "campaign_type" in data_dict:
            campaign_obj.campaign_type = data_dict["campaign_type"]
        if "channel" in data_dict:
            campaign_obj.channel = data_dict["channel"]
        if "status" in data_dict:
            campaign_obj.status = data_dict["status"]
        if "expiring_date" in data_dict:
            campaign_obj.expiring_date = data_dict["expiring_date"]
        # salvo le immagini utilizzando gli id (non le istanze) per migliorare le performance
        if "small_image_id" in data_dict:
            campaign_obj.small_image_id = data_dict["small_image_id"]
        if "large_image_id" in data_dict:
            campaign_obj.large_image_id = data_dict["large_image_id"]
        campaign_obj.save()

        return campaign_obj

    def get_campaign(self, campaign_id):
        """Function to retrieve campaign details"""

        campaign_obj = Campaign()

        if campaign_id:
            try:
                campaign_obj = Campaign.objects.get(campaign_id=campaign_id)
            except Campaign.DoesNotExist:
                # l'oggetto non esiste, notifico l'errore
                logger.error("errore in get_campaign, oggetto non esistente")
                raise 

        return campaign_obj

    def get_campaign_info_dict(self, campaign_id):
        """Function to retrieve campaign details dictionary"""

        campaign_obj = Campaign()
        campaign_info_dict = {}

        if campaign_id:
            try:
                campaign_obj = self.get_campaign(campaign_id=campaign_id)
            except Campaign.DoesNotExist:
                # l'oggetto non esiste, notifico l'errore
                logger.error("errore in get_campaign_info_dict, oggetto non esistente")
                raise 
            else:
                campaign_info_dict = {
                    'campaign_id' : campaign_obj.campaign_id,
                    'camp_title' : campaign_obj.camp_title,
                    'was_price' : campaign_obj.was_price,
                    'final_price' : campaign_obj.final_price,
                    'camp_description' : campaign_obj.camp_description,
                    'small_image_id' : campaign_obj.small_image.campaign_image_id,
                    'large_image_id' : campaign_obj.large_image.campaign_image_id,
                    'small_image_url' : campaign_obj.small_image.image.url,
                    'large_image_url' : campaign_obj.large_image.image.url,
                    'expiring_date' : campaign_obj.expiring_date,
                }

        return campaign_info_dict

class CampaignDest(models.Model):
    campaign_dest_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=25, null=False, blank=False, verbose_name="Il codice univoco generato per il destinatario")
    dest = models.CharField(max_length=50, null=False, blank=False, verbose_name="Dove inviare la promozione")
    channel = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name="Canale di destinazione (email/sms)")
    creation_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'promotion_app'
        indexes = [
            models.Index(fields=['dest',]),
            models.Index(fields=['channel',]),
            models.Index(fields=['code',]),
        ]

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
    channel = models.IntegerField(default=(project_constants.CHANNEL_EMAIL), null=False, blank=False, verbose_name="Canale di destinazione (email/sms)")

    class Meta:
        app_label = 'promotion_app'
        indexes = [
            models.Index(fields=['dest',]),
            models.Index(fields=['channel',]),
        ]

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
        indexes = [
            models.Index(fields=['code',]),
            models.Index(fields=['status',]),
        ]

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
