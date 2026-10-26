from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class CreateTask(BaseModel):
    title: str | None = None

app = FastAPI()
tasks = [
    {"id": 1, "title": "Finish the book", "done": False},
    {"id": 2, "title": "Clean the room", "done": True},
    {"id": 3, "title": "Work out", "done": False}
]

@app.get("/")
async def root():
    return {"name": "Task API",
            "version": "1.0",
            "endpoints": "/tasks"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_tasks(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks")
async def create_task(task_data: CreateTask):
    if task_data.title is None or not task_data.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    new_task = {
        "id": max(task["id"] for task in tasks) + 1,
        "title": task_data.title,
        "done": False
    }

    tasks.append(new_task)

    return JSONResponse(status_code=201, content=new_task)