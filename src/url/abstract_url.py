import abc
import json
from datetime import datetime

from config import DOMAIN
from util import get_random_id, hash_message, hash_and_clean_tag


class AbstractUrl(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, long_url: str = None, metadata: str = None):
        self.__random_id = None
        self.__short_url = None
        self.__tag = None

        self._long_url = long_url
        self._metadata = metadata

    @property
    def random_id(self):
        if self.__random_id is None:
            self.__random_id = get_random_id()
        return self.__random_id

    @random_id.setter
    def random_id(self, random_id):
        self.__random_id = random_id
        self.__short_url = None
        self.__tag = None

    @property
    def short_url(self):
        if self.__short_url is None:
            self.__short_url = DOMAIN + "{}".format(self.random_id)

        return self.__short_url

    @property
    def tag(self):
        if self.__tag is None:
            tag = hash_message(self.random_id)
            self.__tag = hash_and_clean_tag(tag)

        return self.__tag

    @property
    @abc.abstractmethod
    def long_url(self):
        pass

    @property
    @abc.abstractmethod
    def type(self):
        pass

    @property
    @abc.abstractmethod
    def metadata(self):
        pass

    @property
    def message(self):
        message = {
            "long_url": self.long_url,
            "short_url": self.short_url,
            "type": self.type,
            "metadata": self.metadata,
            "timestamp": int(datetime.utcnow().timestamp())
        }

        message["hash"] = hash_message(json.dumps(message))

        return message
