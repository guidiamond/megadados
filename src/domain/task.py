from typing import Optional
from pydantic import BaseModel, Field
import uuid

class Task(BaseModel):
    description: Optional[str] = Field(
        None, title="task description"
    )
    status: Optional[bool] = Field(
        None, title="current task status"
    )
