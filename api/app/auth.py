import functools

from fastapi import Request, Response, HTTPException, WebSocket, status

from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    AuthCredentials,
)

import jwt

import settings
import models
import db


def init(app):
    app.add_middleware(
        AuthenticationMiddleware,
        backend=JWTCookieAuthBackend(),
    )

    @app.post("/auth")
    async def auth(response: Response, user_creds: models.UserCredentials):
        api_user = await lookup_user(user_creds)
        if api_user is not None:
            token = jwt.encode(
                {"user": models.AuthUser(**api_user).dict()},
                str(settings.SECRET_KEY),
                algorithm="HS256",
            )

            response.set_cookie(
                key="token", value=token.decode(), max_age=60 * 60 * 24 * 10
            )
            return {"detail": "authorized"}
        raise HTTPException(status_code=401)


async def lookup_user(user_creds: models.UserCredentials) -> object:
    # idea for integration test:
    # test fetch_one returns None
    return db.database.fetch_one(
        (
            models.api_users.select()
            .where(db.api_users.c.username == user_creds.username)
            .where(db.api_users.c.password == user_creds.password)
        )
    )


class JWTCookieAuthBackend(AuthenticationBackend):
    # fastapi middleware

    async def authenticate(self, request):
        token = request.cookies.get("token", None)

        if token is None:
            return

        try:
            decoded = jwt.decode(
                token, str(settings.SECRET_KEY), algorithms="HS256", verify=True
            )
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationError("Invalid token")

        username, role = decoded["user"]["username"], decoded["user"]["role"]

        return AuthCredentials(["authenticated"]), UserRole(username, role)


class UserRole(SimpleUser):
    def __init__(self, username: str, role: str) -> None:
        self.username = username
        self.role = role

    @property
    def get_role(self):
        return self.role


async def current_user(request: Request):
    # request handler dependency.
    # when dependency loaded as Depend() argument, the auth cookie is checked internally on each request.
    # see AuthenticationBackend docs.
    return request.user


def secure():
    # decoration of fastapi request handler.

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            if not kwargs["current_user"].is_authenticated:
                raise HTTPException(status_code=401)
            return await func(*args, **kwargs)

        return wrapped

    return wrapper


async def check_coockie(websocket: WebSocket):
    # fast api request handler dependency.
    # checks auth coockie for websocket request handler.
    try:
        _ = jwt.decode(
            websocket.cookies.get("token", None),
            str(settings.SECRET_KEY),
            algorithms="HS256",
            verify=True,
        )
    except (jwt.exceptions.InvalidTokenError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise AuthenticationError("Invalid token")
