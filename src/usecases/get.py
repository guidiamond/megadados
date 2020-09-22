from enum import Enum
from fastapi import APIRouter, status
from ..main import main

router = APIRouter()


class TASK_STATUS(str, Enum):
    DONE = "done"
    UNDONE = "undone"


@router.get("/tasks", status_code=status.HTTP_200_OK, tags=["getters"])
def list_all():
    return {"tasks": main.tasks}


@router.get("/tasks/{task_status}", status_code=status.HTTP_200_OK, tags=["getters"])
def list_task_by_status(task_status: TASK_STATUS):
    result_array = {}
    if task_status == TASK_STATUS.DONE:
        task_status = True

    elif task_status == TASK_STATUS.UNDONE:
        task_status = False

    for key, value in main.tasks.items():
        if value.status == task_status:
            result_array[key] = value
    return {"tasks": result_array}
