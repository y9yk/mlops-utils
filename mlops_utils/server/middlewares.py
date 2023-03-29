import jwt
import time
import typing

# from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp

from mlops_utils.constants.strings import *
from mlops_utils.server.exceptions import *


class AuthCheckerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        routes: typing.Sequence[str] = (),
    ) -> None:
        self.app = app
        self.routes = routes

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # inspect routes
        if request.url.path in self.routes:
            try:
                auth_header = request.headers.get("Authorization")
                assert auth_header
                # decode jwt
                access_token = auth_header.split(" ")[1]
                decoded = jwt.decode(
                    jwt=access_token,
                    key=JWT_SECRET,
                    algorithms=[JWT_ALGORITHM],
                )
                # assign decoded str to request object
                request.decoded = decoded
                # return response
                return await call_next(request)
            except:
                raise UnAuthorizedException(
                    message=AUTHENTICATION_REQUIRED,
                )
        else:
            return await call_next(request)


class TimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        res = await call_next(request)
        process_time = time.time() - start_time
        res.headers["X-Process-Time"] = str(process_time)
        return res
