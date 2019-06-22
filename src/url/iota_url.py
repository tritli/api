import iota

from url.url_types import IOTA
from exceptions import URLException
from url.abstract_url import AbstractUrl


class IotaUrl(AbstractUrl):

    TYPE = IOTA

    def __init__(self, address: str = None, tag: str = None, metadata: str = None):

        if address:
            iota_address = iota.Address(address)
            if not iota_address.with_valid_checksum():
                raise URLException("Invalid IOTA address", URLException.INVALID_URL_FORMAT)

        super(IotaUrl, self).__init__(address, tag, metadata)

    @property
    def iota_address(self):
        return self.__long_url

    @property
    def type(self):
        self._type = self.TYPE
        return self._type
