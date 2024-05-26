"""Base Response."""

from pydantic import BaseModel, Field
from starlette import status


class BaseResponse(BaseModel):
    """Base Response."""

    success: bool = Field(default=True)
    status_code: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default="API success")
    data: BaseModel = Field(...)
