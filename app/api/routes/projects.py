from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_project_service
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.response import StandardResponse, ErrorResponse
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", status_code=201, response_model=StandardResponse[ProjectResponse])
def create_project(project_data: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    project = service.create_project(project_data)
    return StandardResponse(data=project, message="project successfully created")


@router.get("", response_model=StandardResponse[List[ProjectResponse]])
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    service: ProjectService = Depends(get_project_service)
):
    projects = service.get_projects(skip, limit, status, search)
    return StandardResponse(data=projects, message="project list retrieved")


@router.get("/{project_id}", response_model=StandardResponse[ProjectResponse])
def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = service.get_project(project_id)
    if project is None:
        error = ErrorResponse(error="project not found", message="project with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data=project, message="project found")


@router.put("/{project_id}", response_model=StandardResponse[ProjectResponse])
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    project = service.update_project(project_id, project_data)
    if project is None:
        error = ErrorResponse(error="project not found", message="project with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data=project, message="project successfully updated")


@router.delete("/{project_id}", response_model=StandardResponse[dict])
def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    if not service.delete_project(project_id):
        error = ErrorResponse(error="project not found", message="project with specified id does not exist")
        raise HTTPException(status_code=404, detail=error.model_dump())
    return StandardResponse(data={}, message="project successfully deleted")

