from __future__ import absolute_import, division, print_function, \
    unicode_literals
from requests.exceptions import ConnectionError
from exceptions import URLException
from iota import BadApiResponse, Iota, Address, Tag, ProposedTransaction, TryteString, Transaction
from config import NODES, TAG
from util import prepare_tag
from url.url_types import IOTA, DOC
from url import Url, IotaUrl, DocumentUrl
from url.url_message import UrlMessage
import json

MAX_LENGTH_SIGNATURE_FRAGMENT = 2187

class NodeManager(object):
    def __init__(self):
        self.__node = None
        self.__depth = 3
        self.__value = 0

    @property
    def node(self):
        # check node responsiveness
        def node_is_responsive(node_to_check: Iota):
            node_uri = node_to_check.adapter.get_uri()

            try:
                node_to_check.get_node_info()
            except ConnectionError as e:
                print("{uri}:{exception}".format(uri=node_uri, exception=e))
                return False
            except BadApiResponse as e:
                print("{uri}:{exception}".format(uri=node_uri, exception=e))
                return False
            else:
                print('{uri} is good to go'.format(uri=node_uri))
                return True

        if self.__node is None:
            for node_uri in NODES:
                node = Iota(node_uri)
                if node_is_responsive(node):
                    self.__node = node
                    print('Selected node: {node}'.format(node=self.__node.adapter.get_uri()))
                    break

        return self.__node

    def send_transaction(self, url):
        address = Address(url.address)
        tag = Tag(url.tag.encode("utf-8"))
        message = TryteString.from_unicode(json.dumps(url.message.json))

        if len(message) > MAX_LENGTH_SIGNATURE_FRAGMENT:
            raise URLException(URLException.MAX_LENGTH)

        proposed_transaction = ProposedTransaction(address=address,
                                                   value=self.__value,
                                                   tag=tag,
                                                   message=message
                                                   )

        self.node.send_transfer(depth=self.__depth,
                                transfers=[proposed_transaction]
                                )

    def retrieve_transactions(self, address: str = None, tag: str = None, number: int = None):

        MAX_TRIES = 20

        def convert_trytes_to_string(tryte_string):
            transaction_to_decode = Transaction.from_tryte_string(tryte_string)
            tag = transaction_to_decode.tag
            message_string = transaction_to_decode.signature_message_fragment.decode()
            return tag, UrlMessage(message_string)

        def convert_to_url_transaction(transaction_hashes, number: int = None):
            trytes = self.node.get_trytes(transaction_hashes)

            if "trytes" not in trytes:
                raise URLException(URLException.CONVERT_ERROR)

            tryte_strings = trytes["trytes"]

            if len(tryte_strings) == 0:
                raise URLException(URLException.CONVERT_ERROR)

            url_transactions = list()
            tries = 0

            for tryte_string in tryte_strings:
                try:
                    tag, message = convert_trytes_to_string(tryte_string)

                    if message.type == IOTA:
                        url = IotaUrl()
                    elif message.type == DOC:
                        url = DocumentUrl()
                    else:
                        url = Url()

                    url.from_message(message)
                    url_transactions.append(url)

                    if (number and len(url_transactions) == number) or tries == MAX_TRIES:
                        return url_transactions

                except Exception as e:
                    print(e)
                    pass
                tries += 1

            return url_transactions

        if address:
            transactions = self.node.find_transactions(addresses=[Address(address)])
        elif tag:
            identifier_tag = prepare_tag(tag).encode("utf-8")
            transactions = self.node.find_transactions(tags=[Tag(identifier_tag)])
        else:
            identifier_tag = prepare_tag(TAG).encode("utf-8")
            transactions = self.node.find_transactions(tags=[Tag(identifier_tag)])

        if "hashes" not in transactions or len(transactions["hashes"]) == 0:
            raise URLException(URLException.URL_NOT_FOUND)

        url_transactions = convert_to_url_transaction(transactions["hashes"], number)

        if not url_transactions:
            raise URLException(URLException.URL_NOT_FOUND)

        return url_transactions

    def transaction_exits(self, address: str = None, tag: str = None):
        if address:
            transactions = self.node.find_transactions(addresses=[Address(address)])
        elif tag:
            identifier_tag = prepare_tag(tag).encode("utf-8")
            transactions = self.node.find_transactions(tags=[Tag(identifier_tag)])
        else:
            identifier_tag = prepare_tag(TAG).encode("utf-8")
            transactions = self.node.find_transactions(tags=[Tag(identifier_tag)])

        if "hashes" not in transactions or len(transactions["hashes"]) == 0:
            return False

        return True

    def last_transactions(self, tag: str = None, number: int = 5):
        url_transactions = self.retrieve_transactions(tag=tag, number=number)
        return url_transactions
