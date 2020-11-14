import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-63a65gcj.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    auth = request.headers['Authorization']

    if not auth:
        raise AuthError({
            'code': 'auth_header_missing',
            'description': 'Authorization Header is missing'
        }, 400)

    result = auth.split(' ')

    if len(result) != 2 or result[0] != 'Bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization Header must contain a header'
        }, 400)

    return result[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    elif permission not in payload:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found'

        })
    return True


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(url.read())


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @ wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
