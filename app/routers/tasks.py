from fastapi import APIRouter, status, HTTPException, Response
from app.schemas import TaskCreate, TaskResponse

router = APIRouter()

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "completed": False,
    },
    {
        "id": 2,
        "title": "Learn DSA",
        "completed": False,
    },
    {
        "id": 3,
        "title": "Practice DSA",
        "completed": True,
    },
]


"""
  FastAPI()
    ↓
Whole application

APIRouter()
    ↓
One group of routes
"""

@router.get("/tasks")
async def get_tasks(
    completed: bool | None = None,
    title: str | None = None
):

    filtered_tasks = tasks

    if completed is not None:

        temp = []

        for task in filtered_tasks:

            if task["completed"] == completed:
                temp.append(task)

        filtered_tasks = temp

    if title is not None:

        temp = []

        for task in filtered_tasks:

            if title.lower() in task["title"].lower():
                temp.append(task)

        filtered_tasks = temp

    return filtered_tasks

@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )

#pydantic converts json to python object
@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
async def create_task(task: TaskCreate):

    new_task = task.model_dump()

    new_task["id"] = len(tasks) + 1

    tasks.append(new_task)

    return new_task

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: TaskCreate):

    for task in tasks:

        if task["id"] == task_id:

            task.update(updated_task.model_dump())

            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
    
@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
    
