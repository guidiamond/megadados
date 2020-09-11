from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from ..main import main
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


class UpdateInterface(BaseModel):
    task_id: Optional[UUID] = Field(None, title="task id")
    description: Optional[str] = Field(
        None, title="task description"
    )
    status: Optional[bool] = Field(
        None, title="current task status"
    )

@router.patch("/task/status", tags=['update'])
def set_status(body: UpdateInterface, status_code=status.HTTP_201_CREATED):
    task_id = body.task_id
    status = body.status
    if not status:
        raise HTTPException(status_code=422, detail="Empty status!")
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    main.tasks[task_id].status = status
    return {"updated": True}

@router.patch("/task/description", tags=['update'])
def set_description(body: UpdateInterface, status_code=status.HTTP_201_CREATED):
    task_id = body.task_id
    description = body.description
    if not description:
        raise HTTPException(status_code=422, detail="Empty status!")
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    main.tasks[task_id].status = description
    return {"updated": True}
