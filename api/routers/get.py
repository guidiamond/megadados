from enum import Enum
from fastapi import APIRouter, status, Depends
from ..main import get_db, DBSession

router = APIRouter()


class TASK_STATUS(str, Enum):
    DONE = "done"
    UNDONE = "undone"


@router.get("", status_code=status.HTTP_200_OK)
def list_all(db: DBSession = Depends(get_db)):
    return {"tasks": db.tasks}


@router.get("/{task_status}", status_code=status.HTTP_200_OK, tags=["getters"])
def list_task_by_status(task_status: TASK_STATUS, db: DBSession = Depends(get_db)):
    result_array = {}
    if task_status == TASK_STATUS.DONE:
        task_status = True

    elif task_status == TASK_STATUS.UNDONE:
        task_status = False

    for key, value in db.tasks.items():
        if value.status == task_status:
            result_array[key] = value
    return {"tasks": result_array}
