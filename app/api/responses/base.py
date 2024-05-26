"""Base Response."""

from typing import TypeVar, Generic

from pydantic import BaseModel, Field
from starlette import status

T = TypeVar('T', bound=BaseModel)


class BaseResponse(BaseModel, Generic[T]):
    """Base Response."""

    success: bool = Field(default=True)
    status_code: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default="API success")
    data: T = Field(...)
