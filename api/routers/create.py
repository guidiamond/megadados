from uuid import uuid1
from fastapi import APIRouter, status, Depends
from ..main import Task, get_db, DBSession

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def create(description: str, db: DBSession = Depends(get_db)):
    task_id = uuid1()
    new_task = Task(description=description, status=False)
    db.tasks[task_id] = new_task
    return {"task_id": task_id}
