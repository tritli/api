from url import Url, UrlAddress
from nodes import NodeManager
from config import ADDRESS_VERSION


class UrlManager(object):

    def __init__(self):
        self.__node_manager = None

    @property
    def node_manager(self):
        if not self.__node_manager:
            self.__node_manager = NodeManager()

        return self.__node_manager

    def publish_url(self, url, random_check: bool = True):

        if random_check:
            while self.short_url_exists(url.short_url):
                # could be more self explanatory to create a new short url
                url.random_id = None

        self.node_manager.send_transaction(url)
        return url.message

    def validate_url(self, short_url: str, long_url: str, custom_salt: str = None):
        random_id = short_url.split("/")[-1]

        url = Url()
        url.random_id = random_id

        url_transactions = self.node_manager.retrieve_transactions(address=url.address)

        if not url_transactions:
            return False

        for url_transaction in url_transactions:
            url_to_validate = Url(custom_salt=custom_salt)
            url_to_validate.from_message(url_transaction.message)
            if url_to_validate.long_url == long_url:
                if url_to_validate.is_valid:
                    return True

        return False

    def short_url_exists(self, short_url: str):
        # todo: check the case if there is no backslash
        random_id = short_url.split("/")[-1]

        url_address = UrlAddress(version=ADDRESS_VERSION, payload=random_id).address

        if self.node_manager.transaction_exits(address=url_address):
            return True

        return False

    def get_url(self, short_url: str):
        random_id = short_url.strip('/').split("/")[-1]

        url = Url(long_url=None, metadata=None)
        url.random_id = random_id

        url_transactions = self.node_manager.retrieve_transactions(address=url.address)

        if not url_transactions:
            return None

        message = dict()

        for url in url_transactions:
            if url.is_valid:
                message = url.message
            else:
                message = url.message

        return message

    def get_long_url(self, short_url: str):
        message = self.get_url(short_url=short_url)

        if message and message.is_valid:
            if message.type == 'iota':
                iota_address = message.json["long_url"]
                deep_link = "{}{}{}".format("iota://", iota_address, "/?message=donation")
                return deep_link

            return message.json["long_url"]
        else:
            return None

    def last_urls(self, tag: str = None, number: int = 5, valid_only: bool = True):
        url_transactions = self.node_manager.last_transactions(tag=tag, number=number)

        if not url_transactions:
            return None

        valid_messages = list()

        for url in url_transactions:
            if valid_only and url.is_valid:
                valid_messages.append(url.message.json)
            elif not valid_only:
                valid_messages.append(url.message.json)

        if not valid_messages or len(valid_messages) == 0:
            return None

        return valid_messages
