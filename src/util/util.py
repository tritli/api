import re
import random
import hashlib
import base64

from iota import AsciiTrytesCodec
from config import TRITLI_SALT, SHORT_URL_LENGTH, SHORT_URL_CHARACTER_SET


# careful here: changes made here, will not be backwards compatible
def get_random_id():
    return ''.join(random.SystemRandom().choice(SHORT_URL_CHARACTER_SET) for _ in range(SHORT_URL_LENGTH))


def hash_message(string_to_hash: str, with_passphrase: bool = True, custom_salt: str = None):
    if with_passphrase:
        if custom_salt:
            string_to_hash = string_to_hash + custom_salt
        else:
            string_to_hash = string_to_hash + TRITLI_SALT

    h = hashlib.sha256()
    h.update(string_to_hash.encode('utf-8'))
    return h.hexdigest()


def clean_string(string_to_clean, final_length):
    # delete numbers not allowed in tag
    cleaned_string = re.sub('\d', '9', string_to_clean)

    # remove special characters
    cleaned_string = re.sub('\W+', '9', cleaned_string)

    # cut to the supported length of 27
    if len(cleaned_string) > final_length:
        cleaned_string = cleaned_string[:final_length]

    # convert to uppercase and fill to 27 characters, if string is too short
    cleaned_string = cleaned_string.upper().ljust(final_length, '9')

    return cleaned_string


def prepare_tag(tag: str):
    tag_length = 27

    return clean_string(tag, tag_length)


def prepare_address(hash_string: str):
    address_length = 81 - 1

    # encode to base64 first
    hashed_string = base64.b64encode(hash_string.encode("utf-8")).decode("utf-8")

    return clean_string(hashed_string, address_length)


def prepare_address_tryte_hash(string_to_address: str):
    address_length = 81 - 1

    h = hashlib.sha256()
    h.update(string_to_address.encode('utf-8'))
    hash_bytes = h.digest()

    codec = AsciiTrytesCodec()
    hash_trytes = codec.encode(input=hash_bytes, errors="strict")[0]

    hash_trytes_string = hash_trytes.decode("utf-8")
    hash_trytes_string = hash_trytes_string.upper().ljust(address_length, '9')

    return hash_trytes_string


def get_key(dictionary: dict, key: str):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return None
