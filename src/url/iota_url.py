from url.abstract_url import AbstractUrl


class IotaUrl(AbstractUrl):

    TYPE = "iota"

    def __init__(self, address: str = None, metadata: str = None):
        self.__address = address
        super(IotaUrl, self).__init__(address, metadata)

    @property
    def address(self):
        return self.__address

    @property
    def long_url(self):
        return self._long_url

    @property
    def type(self):
        return self.TYPE

    @property
    def metadata(self):
        if self._metadata is None:
            self._metadata = ""

        return self._metadata
