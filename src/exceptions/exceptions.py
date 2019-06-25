class TritliException(Exception):

    def __init__(self, error):
        Exception.__init__(self, error['message'])
        self.code = error['code']


class URLException(Exception):

    URL_NOT_FOUND = '-100'
    INVALID_URL_FORMAT = '-1000'
    INVALID_URL_TYPE = '-1500'
    INVALID_URL_MESSAGE = '-2000'

    ERROR_CODE_MAP = {
        URL_NOT_FOUND: "URL not found",
        INVALID_URL_FORMAT: "Could not validate URL format",
        INVALID_URL_TYPE: "Invalid URL type",
        INVALID_URL_MESSAGE: "Message empty or incorrect format",
    }

    __ALL_ERRORS = [URL_NOT_FOUND, INVALID_URL_FORMAT, INVALID_URL_TYPE, INVALID_URL_MESSAGE]

    def __init__(self, errors, message=None):
        if not errors or errors not in self.__ALL_ERRORS:
            if message:
                raise Exception(message)
            else:
                raise Exception("URL Exception")

        message = self.ERROR_CODE_MAP[errors] if not message else message

        self.message = '[{errors}] {message}'.format(errors=errors, message=message)

        super().__init__(message)

        self.errors = errors

    def __str__(self):
        return self.message
