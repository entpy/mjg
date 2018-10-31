# -*- coding: utf-8 -*-

# list of custom exceptions with error code
class UserAlreadyExistsError(Exception):
    """Error in create user."""
    get_error_code = "001"
    pass

class MaEventsCodeDoesNotExistError(Exception):
    """Error in create user."""
    get_error_code = "002"
    pass
