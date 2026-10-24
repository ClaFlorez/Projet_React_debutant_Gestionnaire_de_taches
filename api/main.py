from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = [
    {"id": 1, "title": "Lire le rapport", "done": True},
    {"id": 2, "title": "Vérifier les alertes", "done": False},
]


@app.get("/tasks")
def get_tasks():
    return tasks


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tâche introuvable")


@app.post("/tasks", status_code=201)
def create_task(data: TaskCreate):
    task = {"id": max((t["id"] for t in tasks), default=0) + 1, "title": data.title, "done": False}
    tasks.append(task)
    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    task = find_task(task_id)
    task.update(data.model_dump(exclude_unset=True))
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task = find_task(task_id)
    tasks.remove(task)
    return {"deleted": task_id}
