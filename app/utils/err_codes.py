class Code(object):
    """
    enum code to every custom errors used for Channel Management REST API.
    """
    error_enum = {
        1001: "User Already Exists",
        1002: "User Not Found",
        1003: "channel Not Found",
        1004: "Oops! Unexpected mongodb error occurred",
        1005: "request denied, user doesn't have permission for this request",
        1006: "user already in channel",
        1007: "user not in channel",
        1008: "All channels are private",
        1009: "channel type is undefined",
        1010: "invalid id found, InvalidId error"
    }

    """
    enum code to point to actual http exception codes

    """
    error_enum_http = {
       1001: 422,
       1002: 404,
       1003: 404,
       1004: 500,
       1005: 401,
       1006: 422,
       1007: 422,
       1008: 422,
       1009: 424,
       1010: 500
    }
    @staticmethod
    def return_error_enum(code):
        return Code.error_enum[code]