from uuid import UUID
from fastapi import APIRouter, HTTPException
from ..main import main

router = APIRouter()


@router.delete("/task", tags=["delete"])
def remove(task_id: UUID):
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    del main.tasks[task_id]
    return {"deleted": True}
