from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from ..main import get_db, DBSession

router = APIRouter()


@router.delete("/task", tags=["delete"])
def remove(task_id: UUID, db: DBSession = Depends(get_db)):
    if not task_id in db.tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    del db.tasks[task_id]
    return {"deleted": True}
