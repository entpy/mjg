from anymail.signals import tracking
from django.dispatch import receiver
import logging

# https://anymail.readthedocs.io/en/stable/sending/tracking/#event-tracking

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(tracking)  # add weak=False if inside some other function/class
def handle_bounce(sender, event, esp_name, **kwargs):
    if event.event_type == 'bounced':
        logger.info("Message %s to %s bounced" % (event.message_id, event.recipient))

@receiver(tracking)
def handle_click(sender, event, esp_name, **kwargs):
    if event.event_type == 'clicked':
        logger.info("Recipient %s clicked url %s" % (event.recipient, event.click_url))
