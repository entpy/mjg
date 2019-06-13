from anymail.signals import tracking
from django.dispatch import receiver
from email_app.models import *
import logging

# https://anymail.readthedocs.io/en/stable/sending/tracking/#event-tracking

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(tracking)  # add weak=False if inside some other function/class
def handle_msg_status(sender, event, esp_name, **kwargs):
    logger.info("tracking email status:")
    logger.info(str(event))
    '''In base al msg_id prelevo la mail in email_sent e modifico la bitmask'''
    if event.event_type == 'bounced':
        logger.info("Recipient '%s' msg_id '%s' status bounced" % (event.recipient, event.message_id))
    elif event.event_type == 'delivered':
        logger.info("Recipient '%s' msg_id '%s' status delivered" % (event.recipient, event.message_id))
        email_sent_obj = EmailSent()
        email_sent_obj.add_msg_status_bitmask(msg_id=event.message_id, status_bitmask=project_constants.EMAIL_STATUS_SENT)
    elif event.event_type == 'opened':
        logger.info("Recipient '%s' msg_id '%s' status opened" % (event.recipient, event.message_id))
        email_sent_obj = EmailSent()
        email_sent_obj.add_msg_status_bitmask(msg_id=event.message_id, status_bitmask=project_constants.EMAIL_STATUS_OPEN)
    elif event.event_type == 'clicked':
        logger.info("Recipient '%s' clicked url '%s' msg_id '%s' status clicked" % (event.recipient, event.click_url, event.message_id))
        email_sent_obj = EmailSent()
        email_sent_obj.add_msg_status_bitmask(msg_id=event.message_id, status_bitmask=project_constants.EMAIL_STATUS_CLICK)

    return True
