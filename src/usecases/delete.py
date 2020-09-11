from ..main import main
from fastapi import APIRouter, HTTPException 
from uuid import UUID

router = APIRouter()

@router.delete("/task", tags=["delete"])
def remove(task_id: UUID):
    if not task_id in main.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    del main.tasks[task_id]
    return {"deleted": True}
