from fastapi import APIRouter,status
from ..domain import Task
from ..main import main
from uuid import uuid1

router = APIRouter()

@router.post("/task", status_code=status.HTTP_201_CREATED, tags=["create"])
def create(description: str):
    task_id = uuid1()
    new_task = Task(
        description=description,
        status=False
    )
    main.tasks[task_id] = new_task
    return {"task_id": task_id}
