import json
from functools import wraps
from flask import Flask, request, redirect, abort, jsonify
from flask_restplus import Api, Resource, fields
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from exceptions import URLException
from api.auth import check_api_user
from url import UrlManager, Url, IotaUrl, DocumentUrl
from util import get_key

app = Flask(__name__)

api = Api(
    app=app,
    title='Trit.li API',
    version='0.1',
    contact='Trit.li',
    contact_email='info@trit.li',
    contact_url='https://trit.li')

auth = HTTPBasicAuth()
# you can use the decorator @auth.login_required to require authentication first --> see config

limiter = Limiter(
    app,
    key_func=get_remote_address
    # default_limits=["100 per day", "10 per hour", "1 per minute"]
)

lfs = api.namespace('lfs', description='Get long URL from short URL')
sfl = api.namespace('sfl', description='Get short URL from long URL')
val = api.namespace('val', description='Validate your short URL')
exp = api.namespace('exp', description='Explore last posted URLs')

long_url_body = api.model(
    'LongURL',
    {
        'long_url': fields.String(
            required=True,
            description='Long URL',
            example="http://trit.li/"),

        'custom_salt': fields.String(
            required=False,
            description='Optional: Custom SALT, needed for later validation for generating hash',
            example="tritli_salt"),

        'custom_url': fields.String(
            required=False,
            description='Optional: Custom URL (allowed are letters, numbers, and dashes)',
            example="tritli-123"),

        'tag': fields.String(
            required=False,
            description='Optional: Enter a tag (allowed: [a-zA-Z9])',
            example="TRITLI999999999999999999999"),

        'type': fields.List(fields.String(
            required=True,
            description='Optional: Choose a url type',
            example="url",
            enum=['url', 'iota', 'document'])),

        'metadata': fields.String(
            required=False,
            description='Optional: Attach description (max. length 160 characters)',
            example="trit.li example")
    }
)

short_url_body = api.model(
    'ShortURL',
    {
        'short_url': fields.String(
            required=True,
            description='Short URL',
            example="http://trit.li/JvTULY")
    }
)

validation_body = api.model(
    'URLValidation',
    {
        'short_url': fields.String(
            required=True,
            description='Short URL',
            example="http://trit.li/JvTULY"),

        'long_url': fields.String(
            required=True,
            description='Long URL',
            example="http://trit.li/"),

        'custom_salt': fields.String(
            required=False,
            description='Optional: When a custom salt was used, this is needed to validate the short URL',
            example="tritli_salt")
    }
)

explore_body = api.model(
    'LastURLs',
    {
        'tag': fields.String(
            required=False,
            description='Optional: Search for tag',
            example="TRITLI999999999999999999999"),

        'number': fields.Integer(
            required=False,
            description='Optional: Maximum number of last URLs',
            example=5),

        'valid_only': fields.Boolean(
            required=False,
            description='Optional: Retrieve only trit.li validated last URLs',
            example=False)
    }
)


def limit_content_length(max_length):
    """Decorator, which can be used to check the maximum request length
    :param int max_length: maximum length
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@auth.verify_password
def verify(user_name, password):
    if not (user_name and password):
        return False
    return check_api_user(user_name=user_name, password=password)


@app.errorhandler(Exception)
def handle_error(error):
    """Handles all exception and returns a error message in json format as API response
    :param exception error: the raised exception
    :rtype: response: json containing the error code and the error message
    """
    if isinstance(error, URLException):
        return error.get_response()

    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': type(error).__name__,
            'message': error.args
        }
    }

    return jsonify(response), status_code


@app.route('/<short_url>')
def redirect_short_url(short_url):
    """
    Returns a long URL for a valid short URL and redirects the user automatically to the long URL
    :param object short_url: the short URL
    :rtype: redirect: redirects to the respective long URL
    """
    url_manager = UrlManager()
    long_url = url_manager.get_long_url(short_url="/" + short_url)
    return redirect(long_url)


@lfs.route('/', methods=['POST'])
@lfs.errorhandler(Exception)
class LongFromShort(Resource):
    """Retrieve Long URL from a valid Short URL
    :param dict resource: request body
    """

    @api.expect(short_url_body, validate=True)
    @api.response(200, 'Short URL found')
    def post(self):
        """Post long URL.
        Returns a long URL for a valid short URL.
        :param object request_body: the short URL
        :rtype: json: contains the long URL, the short URL and the metadata
        """
        body = request.get_json()

        short_url = body["short_url"]

        url_manager = UrlManager()
        message = url_manager.get_url(short_url=short_url)
        message = message.json

        status = 200

        response = app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )

        return response


@sfl.route('/', methods=['POST'])
@sfl.errorhandler(Exception)
class ShortFromLong(Resource):
    """Retrieve Short URL for a Long URL
    :param dict resource: request body
    """

    @api.expect(long_url_body, validate=True)
    @api.response(200, 'Short URL generated')
    @limit_content_length(1000)
    @limiter.limit("100/day;10/hour;1/minute")
    def post(self):
        """Post short URL.
        Returns a short URL for a long URL.
        :param object request_body: the long URL with its meta data
        :rtype: json: contains the long URL, the short URL and the metadata
        """
        body = request.get_json()

        long_url = body["long_url"]
        custom_salt = get_key(body, 'custom_salt')
        custom_url = get_key(body, 'custom_url')
        tag = get_key(body, 'tag')
        metadata = get_key(body, 'metadata')
        url_type = body["type"][0]

        if url_type == 'iota':
            url = IotaUrl(address=long_url, tag=tag, metadata=metadata, custom_salt=custom_salt)
        elif url_type == 'document':
            url = DocumentUrl(document_hash=long_url, tag=tag, metadata=metadata, custom_salt=custom_salt)
        else:
            url = Url(long_url=long_url, tag=tag, metadata=metadata, custom_salt=custom_salt)

        if custom_url:
            url.random_id = custom_url

        url_manager = UrlManager()
        message = url_manager.publish_url(url=url)
        message = message.json
        status = 200

        response = app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )

        return response


@val.route('/', methods=['POST'])
@val.errorhandler(Exception)
class ValidateShortURL(Resource):
    """Validates a Short URL with the respective Long URL
    :param dict resource: request body
    """

    @api.expect(validation_body, validate=True)
    @api.response(200, 'URL valid')
    @limiter.limit("100/day;10/hour;1/minute")
    def post(self):
        """Post short URL.
        Returns a short URL for a long URL.
        :param object request_body: contains the short and long URL
        :rtype: json: contains the short, long URL and a bool, if the combination is valid or not
        """
        body = request.get_json()

        short_url = body["short_url"]
        long_url = body["long_url"]
        custom_salt = get_key(body, 'custom_salt')

        url_manager = UrlManager()
        valid = url_manager.validate_url(short_url="/" + short_url, long_url=long_url, custom_salt=custom_salt)

        message = {
            'short_url': short_url,
            'long_url': long_url,
            'valid': valid
        }
        status = 200

        response = app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )

        return response


@exp.route('/', methods=['POST'])
@exp.errorhandler(Exception)
class ExploreURL(Resource):
    """Retrieves the last requested short URLs
    :param dict resource: request body
    """

    @api.expect(explore_body, validate=True)
    @api.response(200, 'Last # URLs loaded')
    def post(self):
        """
        Retrieves the last requested short URLs
        :param object request_body: contains the different parameters: tag, number of entries, valid entries only
        :rtype: json: contains the requested short URL entries, retrieved from the tangle
        """
        body = request.get_json()

        tag = get_key(body, 'tag')
        number = body["number"] if "number" in body else 5
        valid_only = get_key(body, 'valid_only')

        url_manager = UrlManager()
        message = url_manager.last_urls(tag=tag, number=number, valid_only=valid_only)
        status = 200

        response = app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )

        return response
