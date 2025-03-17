from pydantic import BaseModel, EmailStr
from pydantic.types import UUID4
from datetime import datetime
from enum import Enum

class UserRoleStatus(str, Enum):
    USER = "user"
    STUDENT = "student"
    ADMIN = "admin"

class UserSchema(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    role: UserRoleStatus
    user_date_auth: datetime

    class Config:
        from_attributes = True

class UserProfileSchema(BaseModel):
    name: str
    email: EmailStr
    role: UserRoleStatus

    class Config:
        from_attributes = True

class UserProfileUpdateSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserProfileAdminSchema(BaseModel):
    id: UUID4
    role: UserRoleStatus

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserRegistrationSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True