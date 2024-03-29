# -*- coding: utf-8 -*-

# list of custom exceptions with error code
class UserAlreadyExistsError(Exception):
    """Error in create user"""
    get_error_code = "001"
    pass

class MaEventsCodeDoesNotExistError(Exception):
    """Error in create user"""
    get_error_code = "002"
    pass

class UpdateUserDataError(Exception):
    """Error in update user data"""
    get_error_code = "003"
    pass

class GenerateFriendCodeError(Exception):
    """Error in get generate_friend_code"""
    get_error_code = "004"
    pass
