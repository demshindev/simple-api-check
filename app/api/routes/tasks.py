from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.response import StandardResponse, ErrorResponse
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=201, response_model=StandardResponse[TaskResponse])
def create_task(task_data: TaskCreate, service: TaskService = Depends(get_task_service)):
    task = service.create_task(task_data)
    if task is None:
        error = ErrorResponse(error="project not found", message="project with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data=task, message="task successfully created")


@router.get("", response_model=StandardResponse[List[TaskResponse]])
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    service: TaskService = Depends(get_task_service)
):
    tasks = service.get_tasks(skip, limit, project_id, status, priority, search)
    return StandardResponse(data=tasks, message="task list retrieved")


@router.get("/{task_id}", response_model=StandardResponse[TaskResponse])
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if task is None:
        error = ErrorResponse(error="task not found", message="task with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data=task, message="task found")


@router.put("/{task_id}", response_model=StandardResponse[TaskResponse])
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    task = service.update_task(task_id, task_data)
    if task is None:
        error = ErrorResponse(error="task or project not found", message="task with specified id does not exist or project is incorrect")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data=task, message="task successfully updated")


@router.delete("/{task_id}", response_model=StandardResponse[dict])
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    if not service.delete_task(task_id):
        error = ErrorResponse(error="task not found", message="task with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data={}, message="task successfully deleted")

