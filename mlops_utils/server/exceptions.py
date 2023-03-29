from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse
from bentoml.exceptions import BentoMLException
from http import HTTPStatus


class Exception(BaseModel):
    message: str


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            Exception(
                message=exc.detail,
            ),
        ),
    )
