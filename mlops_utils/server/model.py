from fastapi import HTTPException
from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    status: int
    message: str
    data: any
