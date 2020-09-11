from fastapi import FastAPI
from ..usecases import create, get, update, delete

app = FastAPI()

global tasks
tasks = {}

app.include_router(create.router)
app.include_router(get.router)
app.include_router(update.router)
app.include_router(delete.router)
