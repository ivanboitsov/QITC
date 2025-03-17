from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

from models.schemas.task_schemas import TaskSchema

class CourseStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DELETED = "deleted"

class CourseSchema(BaseModel):
    id: int
    name: str
    description: str
    students_count: int
    status: CourseStatus

    class Config:
        from_attributes = True  

class CourseCreateSchema(BaseModel):
    name: str
    description: str
    students_count: int

    class Config:
        from_attributes = True 

class CourseUpdateSchema(BaseModel):
    name: str
    description: str
    students_count: int
    status: CourseStatus

    class Config:
        from_attributes = True 

class CourseWithTasksSchema(BaseModel):
    id: int
    name: str
    description: str
    students_count: int
    status: CourseStatus
    tasks: Optional[List[TaskSchema]]

    class Config:
        from_attributes = True

