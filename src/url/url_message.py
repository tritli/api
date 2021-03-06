import json
from exceptions import URLException
from util import hash_message
from config import TAG
from util import prepare_tag


class UrlMessage(object):
    """
    Defines the data structure, which will be written onto the tangle as a signature message.
    The class itself provides the validation check re-calculating the hash stored on the tangle as well.
    """

    ALL_FIELDS = ["long_url", "short_url", "tag", "type", "metadata", "timestamp", "hash"]
    REQ_FIELDS = ["long_url", "short_url", "type", "metadata", "timestamp"]

    def __init__(self, message, custom_salt: str = None):
        try:
            if not isinstance(message, dict):
                message = json.loads(message)
        except Exception as e:
            raise URLException(URLException.INVALID_URL_MESSAGE, message=str(e))

        if not message or not all(k in message for k in self.REQ_FIELDS):
            raise URLException(URLException.INVALID_URL_MESSAGE)

        self.__long_url = message["long_url"]
        self.__short_url = message["short_url"]
        self.__custom_salt = custom_salt
        self.__tag = message["tag"] if "tag" in message else prepare_tag(TAG)
        self.__type = message["type"]
        self.__metadata = message["metadata"]
        self.__timestamp = message["timestamp"]
        self.__hash = message["hash"] if "hash" in message else None

    @property
    def long_url(self):
        return self.__long_url

    @property
    def tag(self):
        return self.__tag

    @property
    def random_id(self):
        return self.short_url.strip('/').split("/")[-1]

    @property
    def short_url(self):
        return self.__short_url

    @property
    def custom_salt(self):
        return self.__custom_salt

    @custom_salt.setter
    def custom_salt(self, custom_salt):
        self.__custom_salt = custom_salt

    @property
    def type(self):
        return self.__type

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        self.__metadata = metadata

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def json(self):
        return {
            "long_url": self.long_url,
            "short_url": self.short_url,
            "tag": self.tag,
            "type": self.type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "is_valid": self.is_valid
        }

    @property
    def hash(self):
        if not self.__hash:
            message = {
                "long_url": self.long_url,
                "short_url": self.short_url,
                "tag": self.tag,
                "type": self.type,
                "metadata": self.metadata,
                "timestamp": self.timestamp,
            }

            self.__hash = hash_message(json.dumps(message), custom_salt=self.custom_salt)
        return self.__hash

    @hash.setter
    def hash(self, url_hash):
        self.__hash = url_hash

    @property
    def is_valid(self):
        message = {
            "long_url": self.long_url,
            "short_url": self.short_url,
            "tag": self.tag,
            "type": self.type,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

        fresh_hash = hash_message(json.dumps(message), custom_salt=self.custom_salt)

        return self.hash == fresh_hash
