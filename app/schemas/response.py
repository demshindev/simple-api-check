from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class StandardResponse(BaseModel, Generic[T]):
    data: T
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str

