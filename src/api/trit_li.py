from functools import wraps
from flask import Flask, request, redirect, abort
from flask_restplus import Api, Resource, fields
from url import UrlManager, Url, IotaUrl, DocumentUrl
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app=app)

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
    'Long URL',
    {
        'long_url': fields.String(required=True, description='Long URL', example="http://www.example.org/"),
        'tag': fields.String(required=False, description='Enter a tag (allowed: [a-zA-Z9])', example="TRITLI999999999999999999999"),
        'type': fields.List(fields.String(required=True, description='Choose a url type', example="url", enum=['url', 'iota', 'document'])),
        'metadata': fields.String(required=False, description='Attach description (max. length 160 characters)', example="trit.li example")
    }
)

short_url_body = api.model(
    'Short URL',
    {
        'short_url': fields.String(required=True, description='Short URL', example="http://trit.li/oSMJG9")
    }
)

validation_body = api.model(
    'URL Validation',
    {
        'short_url': fields.String(required=True, description='Short URL', example="http://trit.li/oSMJG9"),
        'long_url': fields.String(required=True, description='Long URL', example="http://www.example.org/")
    }
)

explore_body = api.model(
    'Last URLs',
    {
        'tag': fields.String(required=False, description='Find tag', example="TRITLI999999999999999999999"),
        'number': fields.Integer(required=False, description='Number of last URLs', example=5)
    }
)


def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/<short_url>')
def redirect_short_url(short_url):
    url_manager = UrlManager()
    long_url = url_manager.get_long_url(short_url="/" + short_url)
    return redirect(long_url)


@lfs.route('/', methods=['POST'])
class ShortURL(Resource):

    @api.expect(short_url_body, validate=True)
    @api.response(200, 'Short URL found')
    def post(self):
        body = request.get_json()

        short_url = body["short_url"]

        url_manager = UrlManager()
        message = url_manager.get_url(short_url=short_url)

        if message:
            return message.json, 200

        message = {
            "error": "URL not found"
        }

        return message, 200


@val.route('/', methods=['POST'])
class ValidateShortURL(Resource):

    @api.expect(validation_body, validate=True)
    @api.response(200, 'URL valid')
    @limiter.limit("100/day;10/hour;1/minute")
    def post(self):
        body = request.get_json()

        short_url = body["short_url"]
        long_url = body["long_url"]

        url_manager = UrlManager()
        valid = url_manager.validate_url(short_url="/" + short_url, long_url=long_url)

        message = {
            'short_url': short_url,
            'long_url': long_url,
            'valid': valid
        }

        return message, 200


@sfl.route('/', methods=['POST'])
class ShortURL(Resource):

    @api.expect(long_url_body, validate=True)
    @api.response(200, 'Short URL generated')
    @limit_content_length(1000)
    @limiter.limit("100/day;10/hour;1/minute")
    def post(self):
        body = request.get_json()

        long_url = body["long_url"]
        tag = body["tag"] if "tag" in body else None
        metadata = body["metadata"] if "metadata" in body else None
        url_type = body["type"][0]

        if url_type == 'iota':
            url = IotaUrl(address=long_url, tag=tag, metadata=metadata)
        elif url_type == 'document':
            url = DocumentUrl(document_hash=long_url, tag=tag, metadata=metadata)
        else:
            url = Url(long_url=long_url, tag=tag, metadata=metadata)

        url_manager = UrlManager()
        message = url_manager.publish_url(url=url)

        if message:
            return message.json, 200

        message = {
            "error": "URL not found"
        }

        return message, 200


@exp.route('/', methods=['POST'])
class ExploreURL(Resource):

    @api.expect(explore_body, validate=True)
    @api.response(200, 'Last # URLs loaded')
    def post(self):
        body = request.get_json()

        tag = body["tag"] if "tag" in body else None
        number = body["number"] if "number" in body else 5

        url_manager = UrlManager()
        message = url_manager.last_urls(tag=tag, number=number)

        if message:
            return message.json, 200

        message = {
            "error": "URL not found"
        }

        return message, 200
