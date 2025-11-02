from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)
        self.project_repository = ProjectRepository(db)
    
    def create_task(self, task_data: TaskCreate) -> Optional[Task]:
        if self.project_repository.get_by_id(task_data.project_id) is None:
            return None
        return self.task_repository.create(task_data)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)
    
    def get_tasks(self, skip: int = 0, limit: int = 100, project_id: Optional[int] = None, 
                  status: Optional[str] = None, priority: Optional[str] = None, search: Optional[str] = None) -> List[Task]:
        return self.task_repository.get_all(skip, limit, project_id, status, priority, search)
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return None
        
        if task_data.project_id and task_data.project_id != task.project_id:
            if self.project_repository.get_by_id(task_data.project_id) is None:
                return None
        
        return self.task_repository.update(task, task_data)
    
    def delete_task(self, task_id: int) -> bool:
        task = self.task_repository.get_by_id(task_id)
        if task is None:
            return False
        self.task_repository.delete(task)
        return True
    
    def get_task_count(self, project_id: Optional[int] = None, status: Optional[str] = None) -> int:
        return self.task_repository.count(project_id, status)

