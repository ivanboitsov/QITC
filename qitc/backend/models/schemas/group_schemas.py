from typing import List, Optional
from pydantic.types import UUID4
from pydantic import BaseModel

from models.schemas.user_schemas import UserProfileSchema


class GroupCourseWithStudentsSchema(BaseModel):
    id: int
    name: str
    description: str
    students_count: int
    students: Optional[List[UserProfileSchema]]

    class Config:
        from_attributes = True

class GroupSchema(BaseModel):
    user_id: UUID4
    course_id: int

    class Config:
        from_attributes = True