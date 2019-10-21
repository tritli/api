import string

# some sample nodes
NODES = ["https://nodes.thetangle.org:443", "http://node05.iotatoken.nl:16265"]

# NOT YET SUPPORTED - DO NOT USE
# activate local pow to validate transactions on your device
LOCAL_POW = False

# this is the domain used for creating the short URL
DOMAIN = "{}{}".format("http://", "localhost/")

# you can change the default salt used for validation
TRITLI_SALT = "TRITLI"

# default tag to find the url transactions on the tangle (allowed: 27 characters, A-Z and 9 only)
TAG = "TRITLI"

# address prefix, in case of changing the address hash to be backwards compatible
ADDRESS_VERSION = "A"  # T = test, A = alpha

# parameters for creating the short URL
SHORT_URL_LENGTH = 7
SHORT_URL_CHARACTER_SET = string.ascii_letters + string.digits + "-"

# http authentication for the API
# requires usage of the decorator @auth.login_required in trit_li.py
API_USER = "admin"
API_PASS = "admin"

# only affects the flask host and port inside the docker container
# it does not affect the docker image itself
# if you use docker, keep 0.0.0.0
HOST = '0.0.0.0'
PORT = 80
