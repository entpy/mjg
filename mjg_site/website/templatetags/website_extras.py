from django import template
#import logging

# Get an instance of a logger
#logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve a value from a dictionary"""
    return_var = ""
    if dictionary:
        dictionary = vars(dictionary)
        return_var = dictionary.get(key)

    return return_var
