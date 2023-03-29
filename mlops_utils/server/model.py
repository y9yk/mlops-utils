from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    status: int
    message: str
