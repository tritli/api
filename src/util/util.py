import re
import string
import random
import hashlib
import base64
from config import PASSPHRASE


# careful here: changes made here, will not be backwards compatible
def get_random_id():
    size = 6
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def hash_message(string_to_hash: str):
    string_to_hash = string_to_hash + PASSPHRASE
    h = hashlib.sha256()
    h.update(string_to_hash.encode('utf-8'))
    return h.hexdigest()


def prepare_tag(tag: str):
    tag_length = 27

    # delete numbers not allowed in tag
    cleaned_string = re.sub('\d', '9', tag)

    # remove special characters
    cleaned_string = re.sub('\W+', '9', cleaned_string)

    # cut to the supported length of 27
    if len(cleaned_string) > tag_length:
        cleaned_string = cleaned_string[:tag_length]

    # convert to uppercase and fill to 27 characters, if string is too short
    cleaned_string = cleaned_string.upper().ljust(tag_length, '9')

    return cleaned_string


def prepare_address(hash: str):
    address_length = 81 - 1

    # encode to base64
    hashed_string = base64.b64encode(hash.encode("utf-8")).decode("utf-8")

    # delete numbers not allowed in tag
    cleaned_string = re.sub('\d', '9', hashed_string)

    # remove special characters
    cleaned_string = re.sub('\W+', '9', cleaned_string)

    # cut to the supported length of 27
    if len(cleaned_string) > address_length:
        cleaned_string = cleaned_string[:address_length]

    # convert to uppercase and fill to 27 characters, if string is too short
    cleaned_string = cleaned_string.upper().ljust(address_length, '9')

    return cleaned_string
