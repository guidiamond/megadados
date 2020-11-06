# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import uuid

from typing import Dict

from fastapi import APIRouter, HTTPException, Depends

from ..database import DBSession, get_db
from ..models import Task, User

router = APIRouter()


@router.post(
    "",
    summary="Creates a new user",
    description="Creates a new user and returns its UUID.",
    response_model=uuid.UUID,
    status_code=201,
)
async def create_user(name: str, db: DBSession = Depends(get_db)):
    return db.create_new_user(name)


@router.delete(
    "/{uuid_}",
    summary="Deletes user",
    description="Deletes user and his tasks",
    status_code=204,
)
async def remove_user(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.remove_user(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from exception


@router.get(
    "/{uuid_}",
    summary="Reads user tasks",
    description="Reads user tasks from UUID.",
    response_model=Dict[uuid.UUID, Task],
    status_code=200,
)
async def read_user_tasks(
    uuid_: uuid.UUID, completed: bool = None, db: DBSession = Depends(get_db)
):
    try:
        return db.read_user_tasks(uuid_, completed)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        ) from exception


@router.get(
    "/info/{uuid_}",
    summary="Reads user info",
    description="Reads user info from UUID.",
    response_model=User,
    status_code=200,
)
async def read_user_info(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.get_user_info(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from exception


@router.patch(
    "/info/{uuid_}",
    summary="Updates user info",
    description="Updates user info from uuid",
    status_code=204,
)
async def update_user_info(uuid_: str, name: str, db: DBSession = Depends(get_db)):
    try:
        return db.update_user_info(uuid_, name)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from exception
