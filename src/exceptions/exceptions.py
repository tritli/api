from flask import jsonify


class TritliException(Exception):

    def __init__(self, error):
        Exception.__init__(self, error['message'])
        self.code = error['code']


class URLException(Exception):
    API_STATUS_CODE = 400

    URL_NOT_FOUND = '-100'
    INVALID_URL_FORMAT = '-1000'
    INVALID_URL_TYPE = '-1500'
    INVALID_URL_MESSAGE = '-2000'
    CONVERT_ERROR = '-3000'
    MAX_LENGTH = '-4000'

    ERROR_CODE_MAP = {
        URL_NOT_FOUND: "URL not found",
        INVALID_URL_FORMAT: "Could not validate URL format",
        INVALID_URL_TYPE: "Invalid URL type",
        INVALID_URL_MESSAGE: "Message empty or incorrect format",
        CONVERT_ERROR: "Can not convert message from tangle into URL message",
        MAX_LENGTH: "Maximum length of 2187 trytes reached, reduce long_url and/or metadata",
    }

    __ALL_ERRORS = [URL_NOT_FOUND, INVALID_URL_FORMAT, INVALID_URL_TYPE, INVALID_URL_MESSAGE, CONVERT_ERROR, MAX_LENGTH]

    def __init__(self, errors, message=None):
        Exception.__init__(self)
        if not errors or errors not in self.__ALL_ERRORS:
            if message:
                raise Exception(message)
            else:
                raise Exception("URL Exception")

        message = self.ERROR_CODE_MAP[errors] if not message else message

        self.message = '[{errors}] {message}'.format(errors=errors, message=message)
        self.status_code = errors

    def __str__(self):
        return self.message

    def get_response(self):
        ret = {
            "errors": self.status_code,
            "message": self.message
        }
        return jsonify(ret), self.API_STATUS_CODE
