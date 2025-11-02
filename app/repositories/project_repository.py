from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, project_data: ProjectCreate) -> Project:
        project = Project(**project_data.model_dump())
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.db.query(Project).filter(Project.id == project_id).first()
    
    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Project]:
        query = self.db.query(Project)
        
        if status:
            query = query.filter(Project.status == status)
        
        if search:
            search_filter = or_(
                Project.name.ilike(f"%{search}%"),
                Project.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, project: Project, project_data: ProjectUpdate) -> Project:
        data = project_data.model_dump(exclude_unset=True)
        for key, val in data.items():
            setattr(project, key, val)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
    
    def count(self, status: Optional[str] = None) -> int:
        query = self.db.query(Project)
        if status:
            query = query.filter(Project.status == status)
        return query.count()

