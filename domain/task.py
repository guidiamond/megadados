class Task(BaseModel):
    task_id: uuid.UUID = Field(
        None, title="task id", max_length=36
    )
    description: str = Field(
        None, title="task description"
    )
    status: bool
