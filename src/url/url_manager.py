from url import Url
from util import validate_message
from url.abstract_url import AbstractUrl


class UrlManager(object):

    def __init__(self, node_manager):
        self.__node_manager = node_manager
        self.__node = node_manager.node

    def publish_url(self, url: AbstractUrl):

        while self.short_url_exists(url.short_url):
            # could be more self explanatory to create a new short url
            url.random_id = None

        url_transaction = UrlTransaction(tag=url.tag, message=url.message)
        self.__node_manager.send_transaction(url_transaction)
        return url.message

    def validate_url(self, short_url: str, long_url: str):
        random_id = short_url.split("/")[-1]

        url = Url()
        url.random_id = random_id

        url_transactions = self.__node_manager.retrieve_transactions(tag=url.tag)

        if not url_transactions:
            return False

        for url_transaction in url_transactions:
            if url_transaction.message["long_url"] == long_url:
                if validate_message(url_transaction.message):
                    return True

        return False

    def short_url_exists(self, short_url: str):
        # todo: check the case if there is no backslash
        random_id = short_url.split("/")[-1]

        url = Url(long_url=None, metadata=None)
        url.random_id = random_id

        transactions = self.__node_manager.retrieve_transactions(tag=url.tag)

        if transactions:
            return True

        return False

    def get_url(self, short_url: str):
        random_id = short_url.strip('/').split("/")[-1]

        url = Url(long_url=None, metadata=None)
        url.random_id = random_id

        url_transactions = self.__node_manager.retrieve_transactions(tag=url.tag)

        if not url_transactions:
            return None

        valid_message = None

        for url_transaction in url_transactions:
            if validate_message(url_transaction.message):
                valid_message = url_transaction.message

        if not valid_message:
            return None

        return valid_message

    def get_long_url(self, short_url: str):
        message = self.get_url(short_url=short_url)

        if not message:
            return None

        return message["long_url"]


class UrlTransaction(object):

    def __init__(self, tag: str, message: dict):
        self.__tag = tag
        self.__message = message

    @property
    def tag(self):
        return self.__tag

    @property
    def message(self):
        return self.__message
