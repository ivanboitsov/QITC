import logging

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db
from config import oauth2_scheme

from services.auth_service import AuthService
from services.group_service import GroupService
from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema

from models.schemas.group_schemas import GroupCourseWithStudentsSchema, GroupSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

group_router = APIRouter(prefix="/group")


@group_router.post(
    "/student/add",
    tags=["Group"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Student add succesfully"
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def add_student_on_course(
    group_data: GroupSchema,
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    group_service: GroupService = Depends(GroupService)
    ) -> MessageSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Add student to course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Add student to course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        student = await group_service.add_student_to_course(db, group_data.course_id, group_data.user_id)
        if not student:
            logger.warning(f"(Add student to course) Student {group_data.user_id} not added to course {group_data.course_id}")
            raise HTTPException(status_code=400, detail="Invalid input data")
        
        logger.info(f"(Add student to course) Student {group_data.user_id} added to course {group_data.course_id}")
        return MessageSchema(description="Student added successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Add student to course) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@group_router.post(
    "/student/remove",
    tags=["Group"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Student remove succesfully"
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def remove_student_from_course(
    group_data: GroupSchema,
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    group_service: GroupService = Depends(GroupService)
    ) -> MessageSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Remove student from course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Remove student from course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        await group_service.remove_student_from_course(db, group_data.course_id, group_data.user_id)
        logger.info(f"(Remove student from course) Student {group_data.user_id} added to course {group_data.course_id}")
        return MessageSchema(description="Student added successfully")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Remove student from course) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""

@group_router.get(
    "/students/courses",
    tags=["Group"],
    response_model=List[GroupCourseWithStudentsSchema],
    responses={
        200: {
            "model": List[GroupCourseWithStudentsSchema],
            "description": "Get groups succesfully"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_all_groups(
    skip: int = 0,
    limit: int = 10,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    group_service: GroupService = Depends(GroupService)
) -> List[GroupCourseWithStudentsSchema]:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get all groups) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get all groups) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")

        groups = await group_service.get_all_groups(db, skip, limit)
        logger.info(f"(Get all groups) Retrieved {len(groups)} groups")
        return groups

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get all groups) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@group_router.get(
    "/students/{course_id}",
    tags=["Group"],
    response_model=GroupCourseWithStudentsSchema,
    responses={
        200: {
            "model": GroupCourseWithStudentsSchema,
            "description": "Get group succesfully"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_students_list_by_course_id(
    course_id: int,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    group_service: GroupService = Depends(GroupService)
) -> GroupCourseWithStudentsSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get students by course ID) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get students by course ID) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")

        group = await group_service.get_students_by_course_id(db, course_id)
        if not group:
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"(Get students by course ID) Retrieved students for course {course_id}")
        return group

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get students by course ID) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""