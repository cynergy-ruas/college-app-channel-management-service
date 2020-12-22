class Code(object):
    """
    enum code to every custom errors used for ruas-app
    """
    error_enum = {
        1001: "User Already Exists",
        1002: "Wrong Password or Email",
        1003: "channel Not Found",
        1004: "Oops! Unexpected error occurred",
        1005: "User is Locked ! Contact Admin",
        1006: "Not an admin!!Access denied",
        1007: "Fill the missing channel details",
        1008: "No Public channels found!!",
        1009: "channel not found or wrong id"

    }

    @staticmethod
    def ruas_app_error_enum(code):
        return Code.error_enum[code]