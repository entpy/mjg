from django import template
import inspect
#import logging

# Get an instance of a logger
#logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def str_cat(arg1, arg2):
    """Custom filter to concatenate arg1 with arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve a value from a dictionary"""
    return_var = ""
    if dictionary:
        if hasattr(dictionary, '__dict__'):
            dictionary = vars(dictionary)
        else:
            dictionary = dict(dictionary)
        if dictionary.get(key):
            return_var = str(dictionary.get(key))

    return return_var
