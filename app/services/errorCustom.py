
from app.config.err_codes import Code
from pymongo.errors import PyMongoError
class returnExceptions(Exception):
    """
    Custom exception for channel management rest api to be used for specific repeatable
    api related exceptions.
    """
    
    def __init__(self, code=None):
        self.error_code = code

    def __str__(self):
        if self.error_code:
            return '{0}'.format(Code().return_error_enum(self.error_code))
        else:
            return 'Channel Management Custom Error Raised'

