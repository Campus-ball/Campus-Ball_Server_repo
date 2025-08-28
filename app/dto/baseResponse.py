from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    status: int
    message: str
    data: Optional[T]
