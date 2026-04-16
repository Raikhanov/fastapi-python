from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI 
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

tasks:list[TaskSchema] = []

class TaskCreatedSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    completed: Optional[str] = None

@app.get("/tasks")
def read_tasks()-> list[TaskSchema]:
    return tasks


@app.post("/tasks")
def create_task(payload: TaskCreatedSchema)-> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False )
    tasks.append(new_task)

    return new_task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed:
                task.completed = payload.completed
        return task 