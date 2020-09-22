from fastapi import FastAPI, Depends
from ..usecases import create, get, update, delete

tags_metadata = [
    {"name": "create", "description": "task creation method"},
    {"name": "update", "description": "update task description or status by id"},
    {"name": "getters", "description": "get all or filter tasks by status (DONE, UNDONE)"},
    {"name": "delete", "description": "delete a task by task_id method "},
]

app = FastAPI(
    title="Task Manager",
    description="Task manager built in python for better managing your duties",
    openapi_tags=tags_metadata,
)

app.include_router(create.router)
app.include_router(get.router)
app.include_router(update.router)
app.include_router(delete.router)
