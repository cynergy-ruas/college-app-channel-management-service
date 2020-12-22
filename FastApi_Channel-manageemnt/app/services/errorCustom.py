# from fastapi import FastAPI, status

# class Error(Exception):
#     """Base class for other exceptions"""
#     pass

# class RandomError(Error):
#     """Raised when the channel is not found"""
#     pass

# # still in development want this to work for all the errors 
# # so await for this service in next PR. 
# #                                     -ck
from app.config.custom_err import Code

class RuasAppExceptions(Exception):
    """
    Custom exception for RUAS App to be used for specific repeatable
    app related exceptions.
    """

    def __init__(self, *args):
        if args:
            self.error_code = args[0]
        else:
            self.error_code = None

    def __str__(self):
        if self.error_code:
            return '{0}'.format(Code().ruas_app_error_enum(self.error_code))
        else:
            return 'RUAS App Custom Error Raised'
