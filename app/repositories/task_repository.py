from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_by_project_id(self, project_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.project_id == project_id).all()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Task]:
        query = self.db.query(Task)
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        if search:
            search_filter = or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, task: Task, task_data: TaskUpdate) -> Task:
        data = task_data.model_dump(exclude_unset=True)
        for key, val in data.items():
            setattr(task, key, val)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
    
    def count(self, project_id: Optional[int] = None, status: Optional[str] = None) -> int:
        query = self.db.query(Task)
        if project_id:
            query = query.filter(Task.project_id == project_id)
        if status:
            query = query.filter(Task.status == status)
        return query.count()

