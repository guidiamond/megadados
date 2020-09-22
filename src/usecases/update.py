from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status, Depends
from ..main import get_db, DBSession

router = APIRouter()


class UpdateInterface(BaseModel):
    task_id: Optional[UUID] = Field(None, title="task id")
    description: Optional[str] = Field(None, title="task description")
    status: Optional[bool] = Field(None, title="current task status")


@router.patch("/task/status", tags=["update"])
def set_status(
    body: UpdateInterface, db: DBSession = Depends(get_db), status_code=status.HTTP_200_OK
):
    task_id = body.task_id
    body_status = body.status
    if not body_status:
        raise HTTPException(status_code=422, detail="Empty status!")
    if not task_id in db.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    db.tasks[task_id].status = body_status
    return {"updated": True}


@router.patch("/task/description", tags=["update"])
def set_description(
    body: UpdateInterface, db: DBSession = Depends(get_db), status_code=status.HTTP_200_OK
):
    task_id = body.task_id
    description = body.description
    if not description:
        raise HTTPException(status_code=422, detail="Empty description!")
    if not task_id in db.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")
    db.tasks[task_id].description = description
    return {"updated": True}
