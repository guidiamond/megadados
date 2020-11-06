# pylint: disable=missing-module-docstring,missing-class-docstring
from typing import Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


# pylint: disable=too-few-public-methods
class Task(BaseModel):
    owner: Optional[str] = Field("No owner", title="Owner id", max_length=36)
    description: Optional[str] = Field(
        "no description",
        title="Task description",
        max_length=1024,
    )
    completed: Optional[bool] = Field(
        False,
        title="Shows whether the task was completed",
    )

    class Config:
        schema_extra = {
            "example": {
                "description": "Buy baby diapers",
                "completed": False,
            }
        }


class User(BaseModel):
    name: Optional[str] = Field(
        "no name", title="user name", max_length=round(92.4432532432432)
    )

    class Config:
        schema_extra = {
            "example": {
                "description": "Buy baby diapers",
                "completed": False,
            }
        }
