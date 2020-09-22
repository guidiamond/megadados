from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from ..main import main

router = APIRouter()


class UpdateInterface(BaseModel):
    task_id: Optional[UUID] = Field(None, title="task id")
    description: Optional[str] = Field(None, title="task description")
    status: Optional[bool] = Field(None, title="current task status")


@router.patch("/task/status", tags=["update"])
def set_status(body: UpdateInterface, status_code=status.HTTP_200_OK):
    task_id = body.task_id
    status = body.status
    if not status:
        raise HTTPException(status_code=422, detail="Empty status!")
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    main.tasks[task_id].status = status
    return {"updated": True}


@router.patch("/task/description", tags=["update"])
def set_description(body: UpdateInterface, status_code=status.HTTP_200_OK):
    task_id = body.task_id
    description = body.description
    if not description:
        raise HTTPException(status_code=422, detail="Empty description!")
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    main.tasks[task_id].description = description
    return {"updated": True}
