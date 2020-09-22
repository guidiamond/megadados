from uuid import uuid1
from fastapi import APIRouter, status, Depends
from ..domain import Task
from ..main import get_db, DBSession

router = APIRouter()


@router.post("/task", status_code=status.HTTP_201_CREATED, tags=["create"])
def create(description: str, db: DBSession = Depends(get_db)):
    task_id = uuid1()
    new_task = Task(description=description, status=False)
    db.tasks[task_id] = new_task
    return {"task_id": task_id}
