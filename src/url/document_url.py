from url.url_types import DOC
from url.abstract_url import AbstractUrl


class DocumentUrl(AbstractUrl):

    TYPE = DOC

    def __init__(self, document_hash: str = None, tag: str = None, metadata: str = None, custom_salt: str = None):
        self.__document_hash = document_hash

        super(DocumentUrl, self).__init__(document_hash, tag, metadata, custom_salt)

    @property
    def document_hash(self):
        return self.__long_url

    @property
    def type(self):
        self._type = self.TYPE
        return self._type
