from typing import List
from pydantic import BaseModel

from src.task.task_dto import TaskResponse

class CourseResponse(BaseModel):
    id: int
    name: str
    description: str
    students_count: int
    status: str
    tasks: List[TaskResponse]  # Список задач

    class Config:
        orm_mode = True  # Включаем поддержку ORM