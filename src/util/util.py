import re
import json
import string
import random
import hashlib
import base64
from config import PASSPHRASE


def get_random_id():
    size = 6
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def hash_message(string_to_hash: str):
    string_to_hash = string_to_hash + PASSPHRASE
    h = hashlib.sha256()
    h.update(string_to_hash.encode('utf-8'))
    return h.hexdigest()


def hash_and_clean_tag(tag: str):
    # encode to base64
    hashed_string = base64.b64encode(tag.encode("utf-8")).decode("utf-8")

    # delete numbers not allowed in tag
    cleaned_string = re.sub('\d', '', hashed_string)

    # cut to the supported length of 27
    if len(cleaned_string) > 27:
        cleaned_string = cleaned_string[:27]

    # convert to uppercase and fill to 27 characters, if string is too short
    cleaned_string = cleaned_string.upper().ljust(27, '9')

    return cleaned_string


def validate_message(message: dict):
    if not all(k in message for k in ("long_url", "short_url", "type", "timestamp", "hash")):
        return False

    message_to_validate = {
        "long_url": message["long_url"],
        "short_url": message["short_url"],
        "type": message["type"],
        "metadata": message["metadata"],
        "timestamp": message["timestamp"]
    }

    hash_to_validate = message["hash"]

    message_to_validate_string = json.dumps(message_to_validate)
    message_hash = hash_message(message_to_validate_string)

    return message_hash == hash_to_validate
