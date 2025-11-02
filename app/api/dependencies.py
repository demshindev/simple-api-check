from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

