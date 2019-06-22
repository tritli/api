

class TritliException(Exception):

    def __init__(self, error):
        Exception.__init__(self, error['message'])
        self.code = error['code']


class URLException(Exception):

    INVALID_URL_FORMAT = -1000
    INVALID_URL_TYPE = -1500
    INVALID_URL_MESSAGE = -2000

    def __init__(self, msg, code=None):
        self.msg = msg
        self.code = code
        self.s = """
        Error: {msg}
        Code: {code}
        """.format(msg=msg, code=code)

    def __str__(self):
        return self.s
