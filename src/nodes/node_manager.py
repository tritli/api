from __future__ import absolute_import, division, print_function, \
    unicode_literals
from requests.exceptions import ConnectionError
from iota import BadApiResponse, Iota, Address, Tag, ProposedTransaction, TryteString, Transaction
from url import UrlTransaction
from config import NODES, ADDRESS

import pprint as pp
import json


class NodeManager(object):
    def __init__(self):
        self.__node = None
        self.__depth = 3
        self.__value = 0

    @property
    def node(self):
        # check node responsiveness
        def node_is_responsive(node_to_check: Iota, node_uri: str):
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
                if node_is_responsive(node, node_uri):
                    self.__node = node
                    continue

        return self.__node

    def send_transaction(self, url_transaction: UrlTransaction):
        proposed_transaction = ProposedTransaction(address=Address(ADDRESS),
                                                   value=self.__value,
                                                   tag=Tag(url_transaction.tag.encode("utf-8")),
                                                   message=TryteString.from_unicode(json.dumps(url_transaction.message))
                                                   )

        self.node.send_transfer(depth=self.__depth,
                                transfers=[proposed_transaction]
                                )

    def retrieve_transactions(self, tag: str = None):

        def convert_trytes_to_string(tryte_string):
            transaction_to_decode = Transaction.from_tryte_string(tryte_string)
            return transaction_to_decode.signature_message_fragment.decode()

        def convert_to_url_transaction(tag, transaction_hashes):
            trytes = self.node.get_trytes(transaction_hashes)

            if "trytes" not in trytes:
                return None

            tryte_strings = trytes["trytes"]

            if len(tryte_strings) == 0:
                return None

            url_transactions = list()

            for tryte_string in tryte_strings:
                message = convert_trytes_to_string(tryte_string)
                url_transactions.append(UrlTransaction(tag=tag, message=json.loads(message)))

            return url_transactions

        if tag:
            transactions = self.node.find_transactions(tags=[Tag(tag)])
        else:
            transactions = self.node.find_transactions(addresses=[Address(ADDRESS)])

        if "hashes" not in transactions or len(transactions["hashes"]) == 0:
            return None

        url_transactions = convert_to_url_transaction(tag, transactions["hashes"])

        if not url_transactions:
            return None

        return url_transactions

    def last_transactions(self, page: int = 0, page_size: int = 5):
        start = 0
        if page and page > 0:
            start = page_size * (page - 1)

        end = start + page_size

        transactions = self.node.find_transactions(addresses=[Address(ADDRESS)])

        hashes = transactions["hashes"][start:end]
        pp.pprint(hashes)
        # trytes = self.__api.get_trytes(hashes)

        # for tryte_string in trytes["trytes"]:
        #     transaction = Transaction.from_tryte_string(tryte_string)
        #     message = transaction.signature_message_fragment.decode()
        #     pp.pprint(json.loads(message))

