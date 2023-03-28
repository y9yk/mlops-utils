import jwt
import time

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from mlops_utils.constants.strings import *


class AuthCheckerMiddleware(BaseHTTPMiddleware):
    async def dispath(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
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
            raise HTTPException(
                status_code=401,
                detail=AUTHENTICATION_REQUIRED,
            )


class TimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        res = await call_next(request)
        process_time = time.time() - start_time
        res.headers["X-Process-Time"] = str(process_time)
        return res
