import abc
from datetime import datetime
from url.url_message import UrlMessage
from config import DOMAIN, TAG, ADDRESS_VERSION
from util import get_random_id, hash_message, prepare_address, prepare_tag, prepare_address_tryte_hash
from exceptions import URLException


class AbstractUrl(metaclass=abc.ABCMeta):
    """
    Defines the data structure an URL object can have.
    This class only implements the "core" methods other URL types use.

    The different types are:
        - a standard URL using a shortened URL
        - an IOTA address itself for deep links to a wallet using a shortened URL
        - an document or better, its hash for storing document hashes on the tangle using shortened URLs
    """

    @abc.abstractmethod
    def __init__(self, long_url: str = None, tag: str = None, metadata: str = None, custom_salt: str = None):
        self.__random_id = None
        self.__short_url = None
        self.__tag = tag
        self.__address = None
        self.__long_url = long_url
        self.__custom_salt = custom_salt
        self._type = None
        self.__metadata = metadata
        self.__timestamp = None
        self.__message = None

    @property
    def random_id(self):
        if self.__random_id is None:
            self.__random_id = get_random_id()
        return self.__random_id

    @random_id.setter
    def random_id(self, random_id):
        self.__random_id = random_id
        self.__short_url = None
        self.__address = None

    @property
    def short_url(self):
        if self.__short_url is None:
            self.__short_url = "{}".format(self.random_id)

        return self.__short_url

    @short_url.setter
    def short_url(self, short_url: str):
        self.__short_url = short_url

    @property
    def tag(self):
        if self.__tag is None:
            self.__tag = TAG

        return prepare_tag(self.__tag)

    @property
    def timestamp(self):
        if self.__timestamp is None:
            self.__timestamp = int(datetime.utcnow().timestamp())

        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str):
        self.__timestamp = timestamp

    @property
    def address(self):
        if self.__address is None:
            url_address = UrlAddress(version=ADDRESS_VERSION, payload=self.random_id)
            self.__address = url_address.address

        return self.__address

    @property
    def long_url(self):
        return self.__long_url

    @long_url.setter
    def long_url(self, long_url):
        self.__long_url = long_url

    @property
    def custom_salt(self):
        return self.__custom_salt

    @custom_salt.setter
    def custom_salt(self, custom_salt):
        self.__custom_salt = custom_salt

    @property
    @abc.abstractmethod
    def type(self):
        pass

    @type.setter
    def type(self, url_type):
        self._type = url_type

    @property
    def metadata(self):
        if self.__metadata is None:
            self.__metadata = ""

        return self.__metadata

    @metadata.setter
    def metadata(self, metadata):
        self.__metadata = metadata

    @property
    def message(self):
        if not self.__message:
            message = {
                "long_url": self.long_url,
                "short_url": self.short_url,
                "tag": self.tag,
                "type": self.type,
                "metadata": self.metadata,
                "timestamp": self.timestamp
            }

            self.__message = UrlMessage(message, self.custom_salt)

        return self.__message

    def from_message(self, message: UrlMessage):
        self.__message = message
        self.__message.custom_salt = self.__custom_salt
        self.random_id = self.__message.random_id
        self.long_url = self.__message.long_url
        self._type = self.__message.type
        self.metadata = self.__message.metadata
        self.timestamp = self.__message.timestamp

    @property
    def is_valid(self):
        return self.message.is_valid


class UrlAddress(object):
    """
    Defines the structure of an URL address
    An address can have different versions, which defines how the address is retrieved

    Current versions are:
        - T for Test:
            - sha256 hash of the random string using salt from config or custom salt
            - base64 encoding
            - clean string (replacing numbers, uppercase and adapting length)
        - A for Alpha:
            - sha256 hash of the random string using salt from config or custom salt
            - direct conversion into trytes using the pyote library and then length adaption
    """

    TEST = 'T'
    ALPHA = 'A'
    BETA = 'B'

    VERSION_MAP = {
        TEST: 'test',
        ALPHA: 'alpha',
        BETA: 'beta'
    }

    def __init__(self, version: str = None, payload: str = None):
        """
        :param version:
            Version of the URL address
        :param payload:
            String to use as the actual address
        """
        self.__version = version
        self.__payload = payload
        self.__address = None

    @property
    def address(self):
        # type: () -> str
        """
        Returns the calculated IOTA compatible address based on the defined version
        """
        if not self.__address:
            if self.version == self.TEST:
                pre_address = hash_message(self.__payload)
                self.__address = self.TEST + prepare_address(pre_address)
            if self.version == self.ALPHA:
                self.__address = self.ALPHA + prepare_address_tryte_hash(self.__payload)
        return self.__address

    @address.setter
    def address(self, address):
        """
        sets the address string
        """
        self.__address = address

    @property
    def version(self):
        # type: () -> str
        """
        Returns the version of an URL address based on the first character in the address
        """
        if not self.__version:
            if self.address[0] in self.VERSION_MAP.keys():
                self.__version = self.VERSION_MAP[self.address[0]]
            else:
                raise URLException(URLException.INVALID_URL_ADDRESS)

        return self.__version

