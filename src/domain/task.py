from typing import Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    description: Optional[str] = Field(None, title="task description")
    status: Optional[bool] = Field(None, title="current task status")
