from typing import Optional, List
import uuid
from enum import Enum

from fastapi import FastAPI, status
from pydantic import BaseModel

# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

app = FastAPI()

# class Task(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


class Task(BaseModel):
    uuid: uuid.UUID
    description: str
    status: bool


class CreateTask(BaseModel):
    description: str


class RemoveTask(BaseModel):
    task_id: str


class AlterDescription(BaseModel):
    task_id: str
    description: str


class SetTaskStatus(BaseModel):
    task_id: str
    status: bool


class TASK_STATUS(str, Enum):
    DONE = "done"
    NOTDONE = "notdone"
    ALL = "all"


class ListTasks(BaseModel):
    status: TASK_STATUS


tasks: List[Task] = []


def get_task_idx(task_id: str) -> int:
    for i in range(len(tasks)):
        if (str(tasks[i].uuid) == task_id):
            return i
    return -1


@app.patch("/set_status")
def set_status(body: SetTaskStatus):
    task_uuid = body.task_id
    status = body.status
    task_idx = get_task_idx(task_uuid)
    if (task_idx == -1):
        return {"status": "nenhum encontrado!"}
    tasks[task_idx].status = status
    return {"status": "ok"}


@app.delete("/delete")
def remove(body: RemoveTask):
    task_uuid = body.task_id
    task_idx = get_task_idx(task_uuid)
    if (task_idx == -1):
        return {"status": "nenhum encontrado!"}
    del tasks[task_idx]
    return {"status": "ok!"}


@app.patch("/alter_description")
def alter_description(body: AlterDescription):
    task_uuid = body.task_id
    task_idx = get_task_idx(task_uuid)
    if (task_idx == -1):
        return {"status": "nenhum encontrado!"}
    tasks[task_idx].description = body.description
    return {"status": "ok!"}


@app.put("/create", status_code=status.HTTP_201_CREATED)
async def create(body: CreateTask):
    description = body.description
    uuid1 = uuid.uuid1()
    new_task = Task(
        uuid=uuid1,
        description=description,
        status=False
    )
    tasks.append(new_task)
    return {"task_id": uuid1}


@app.get("/list/{task_status}")
def list_tasks(task_status: TASK_STATUS):
    # print(task_status)
    if (task_status == TASK_STATUS.DONE):
        ret: List[Task] = [i for i in tasks if i.status == True]
        return {"tasks": ret}

    elif (task_status == TASK_STATUS.NOTDONE):
        ret: List[Task] = [i for i in tasks if i.status == False]
        return {"tasks": ret}
    elif (task_status == TASK_STATUS.ALL):
        return {"tasks": tasks}


@app.get("/list")
def list_all():
    return {"tasks": tasks}
