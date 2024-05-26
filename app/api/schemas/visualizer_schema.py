from typing import Optional

from pydantic import BaseModel, Field, field_validator


class QuestionInputSchema(BaseModel):
    """Question Input Schema."""

    video_path: str = Field(...)
    bot_id: str = Field(...)

    class Config:
        """Config."""
        validate_default = True

    @field_validator("openai_model_name")
    def convert_to_default_if_not_exist(cls, value: str) -> str:
        if value in {
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0125",
        }:
            return value
        else:
            return "gpt-3.5-turbo-1106"

    @field_validator("temperature")
    def divide_temperature_if_more_than_one(cls, value: float) -> float:
        return value / 100 if value > 1 else max(value, 0.2)

    @field_validator("language")
    def convert_to_appropriate_if_not_exist(cls, value: str) -> str:
        return value or "appropriate"
