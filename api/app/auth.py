import functools

from fastapi import Request, Response, HTTPException

from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials)

import jwt

import settings
import models
import db


def init(app):
    app.add_middleware(
        AuthenticationMiddleware,
        backend=JWTCookieAuthBackend(),
    )

    @app.post('/auth')
    async def auth(response: Response, user_creds: models.UserCredentials):
        api_user = await lookup_user(user_creds)
        if api_user is not None:
            token = jwt.encode({'user': models.AuthUser(**api_user).dict()},
                               str(settings.SECRET_KEY), algorithm='HS256')

            response.set_cookie(key='token', value=token.decode(), max_age=60 * 60 * 24 * 10)
            return {'detail': 'authorized'}
        raise HTTPException(status_code=401)


async def lookup_user(user_creds: models.UserCredentials):
    query = models.api_users.select().where(models.api_users.c.username == user_creds.username)
    user = await db.database.fetch_one(query)
    if user:
        return user
    else:
        return None


class JWTCookieAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        token = request.cookies.get('token', None)

        if token is None:
            return

        try:
            decoded = jwt.decode(token, str(settings.SECRET_KEY), algorithms='HS256')
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationError('Invalid token')

        username, role = decoded['user']['username'], decoded['user']['role']

        return AuthCredentials(["authenticated"]), UserRole(username, role)


async def current_user(request: Request):
    ''' Request handler dependency'''
    return request.user


def secure():
    '''
    Request handler decorator.

    Decorated handler needs auth cookie to return 200

    '''
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if isinstance(kwargs['current_user'], UnauthenticatedUser):
                raise HTTPException(status_code=401)
            return await func(*args, **kwargs)
        return wrapped
    return wrapper


class UserRole(SimpleUser):
    def __init__(self, username: str, role: str) -> None:
        self.username = username
        self.role = role

    @property
    def role(self):
        return self.role
