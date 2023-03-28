import jwt
import time

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from mlops_utils.constants.strings import *


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        assert decoded_token["expires"] > time.time()
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=401,
            detail=INVALID_TOKEN_OR_EXPIRED_TOKEN,
        )


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == BEARER:
                raise HTTPException(
                    status_code=401,
                    detail=INVALID_AUTHENTICATION_SCHEME,
                )
            token = credentials.credentials
            request.token = token
            request.decoded = decodeJWT(token)
        else:
            raise HTTPException(
                status_code=401,
                detail=INVALID_AUTHORIZATION_CODE,
            )
