#Imported Modules
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

#Class Creation (Task creation & Task Update)
class CreateTask(BaseModel):
    title: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    done: bool | None = None

#Task List
app = FastAPI()
tasks = [
    {"id": 1, "title": "Finish the book", "done": False},
    {"id": 2, "title": "Clean the room", "done": True},
    {"id": 3, "title": "Work out", "done": False}
]

#Initial GET Function
@app.get("/", summary="Get API Information")
async def root():
    return {"name": "Task API",
            "version": "1.0",
            "endpoints": "/tasks"}

#Health Status
@app.get("/health", summary="Checks health status")
async def health():
    return {"status": "ok"}

#GET Tasks Function
@app.get("/tasks", summary="Retrieves all tasks")
async def get_tasks():
    return tasks

#GET Tasks ID Function
@app.get("/tasks/{id}", summary="Retrieves task by ID")
async def get_tasks(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

#POST Function
@app.post("/tasks", summary="Creates a new task")
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

#PUT Function
@app.put("/tasks/{id}", summary="Updates task by ID")
async def update_task(id: int, task_data: UpdateTask):
    task = next((task for task in tasks if task["id"] == id), None)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    if task_data.title is None and task_data.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "At least one field is required"}
        )

    if task_data.title is not None:
        if not task_data.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )
        task["title"] = task_data.title

    if task_data.done is not None:
        task["done"] = task_data.done

    return task

#DELETE Function
@app.delete("/tasks/{id}", status_code=204, summary="Deletes task by ID")
async def delete_task(id: int):
    task = next((task for task in tasks if task["id"] == id), None)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    tasks.remove(task)
    return None