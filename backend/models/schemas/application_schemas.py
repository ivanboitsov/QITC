from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    NEW = "new"
    READED = "readed"

class ApplicationCreateSchema(BaseModel):
    user_name: str
    phone_number: str
    email: EmailStr
    course_id: int

    class Config:
        from_attributes = True

class ApplicationSchema(BaseModel):
    id: int
    user_name: str
    phone_number: str
    email: EmailStr
    course_id: int
    status: ApplicationStatus
    application_date: datetime

    class Config:
        from_attributes = True