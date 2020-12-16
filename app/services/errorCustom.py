from fastapi import FastAPI, status

class Error(Exception):
    """Base class for other exceptions"""
    pass

class RandomError(Error):
    """Raised when the channel is not found"""
    pass

# still in development want this to work for all the errors 
# so await for this service in next PR. 
#                                     -ck