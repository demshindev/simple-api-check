from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.repository = ProjectRepository(db)
    
    def create_project(self, project_data: ProjectCreate) -> Project:
        return self.repository.create(project_data)
    
    def get_project(self, project_id: int) -> Optional[Project]:
        return self.repository.get_by_id(project_id)
    
    def get_projects(self, skip: int = 0, limit: int = 100, status: Optional[str] = None, search: Optional[str] = None) -> List[Project]:
        return self.repository.get_all(skip, limit, status, search)
    
    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        project = self.repository.get_by_id(project_id)
        if project is None:
            return None
        return self.repository.update(project, project_data)
    
    def delete_project(self, project_id: int) -> bool:
        project = self.repository.get_by_id(project_id)
        if project is None:
            return False
        self.repository.delete(project)
        return True
    
    def get_project_count(self, status: Optional[str] = None) -> int:
        return self.repository.count(status)

