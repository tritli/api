import validators
from validators.utils import ValidationFailure
from url.abstract_url import AbstractUrl


class Url(AbstractUrl):

	TYPE = "url"

	def __init__(self, long_url: str = None, metadata: str = None):
		# todo: check for null or not?!
		try:
			if long_url:
				validators.url(long_url)
		except ValidationFailure as vf:
			raise vf

		super(Url, self).__init__(long_url, metadata)

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
