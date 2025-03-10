from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    CLOSED = "closed"
    INPROCESS = "inProcess"
    DONE = "done"
    DELETED = "deleted"

class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    course_id: int
    status: TaskStatus

    class Config:
        from_attributes = True

class TaskUpdateSchema(BaseModel):
    name: str
    description: str
    course_id: int
    status: TaskStatus

    class Config:
        from_attributes = True

class TaskCreateSchema(BaseModel):
    name: str
    description: str
    course_id: int

    class Config:
        from_attributes = True