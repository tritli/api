import validators

from url.url_types import URL
from exceptions import URLException
from url.abstract_url import AbstractUrl
from validators.utils import ValidationFailure


class Url(AbstractUrl):

	TYPE = URL

	def __init__(self, long_url: str = None, tag: str = None, metadata: str = None, custom_salt: str = None):
		# todo: check for null or not?!
		try:
			if long_url:
				validators.url(long_url)
		except ValidationFailure as vf:
			raise URLException(URLException.INVALID_URL_FORMAT, message=str(vf))

		super(Url, self).__init__(long_url, tag, metadata, custom_salt)

	@property
	def type(self):
		self._type = self.TYPE
		return self._type
