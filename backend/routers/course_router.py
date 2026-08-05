import logging
import traceback

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db
from config import oauth2_scheme

from services.auth_service import AuthService
from services.course_service import CourseService
from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema 
from models.schemas.course_schemas import CourseWithTasksSchema, CourseCreateSchema, CourseSchema, CourseUpdateSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

course_router = APIRouter(prefix="/course")


@course_router.post(
    "",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course created successfully"
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
async def create_course(
    course_data: CourseCreateSchema,
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    """
    Создание курса (только для администратора)
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Create course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Create course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        course = await course_service.create_course(
            db = db, 
            name=course_data.name,
            description=course_data.description,
            students_count=course_data.students_count,
        )

        logger.info(f"(Create course) Course successfully created: {course.id}")

        return MessageSchema(
            messageDigest=str(course.id),
            description=f"(Create course) Course '{course.name}' created successfully"
        )

    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Create course) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Create course) Error: {e}")
        logger.error(traceback.format_exc()) 
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.get(
    "",
    tags=["Course"],
    response_model=List[CourseSchema],
    responses={
        200: {
            "model": List[CourseSchema]
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
async def get_courses(
    skip: int = 0, 
    limit: int = 25,
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseSchema]:
    """
    Просмотр всех курсов (только для администратора)
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get courses) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get courses) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        courses = await course_service.get_courses(db, skip=skip, limit=limit)

        logger.info(f"(Get courses) Successfully retrieved {len(courses)} courses")
        return courses
    
    except Exception as e:
        logger.error(f"(Get courses) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.get(
    "/tasks",
    tags=["Course"],
    response_model=List[CourseWithTasksSchema],
    responses={
        200: {
            "model": List[CourseWithTasksSchema],
            "description": "List of courses with tasks"
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
async def get_courses_with_tasks(
    skip: int = 0,
    limit: int = 5,
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseWithTasksSchema]:
    """
    Просмотр всех курсов с их задачами
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get courses with tasks) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        courses = await course_service.get_courses_with_tasks(db, skip=skip, limit=limit)

        logger.info(f"(Get courses with tasks) Successfully retrieved {len(courses)} courses")
        return courses

    except Exception as e:
        logger.error(f"(Get courses with tasks) Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.get(
    "/active",
    tags=["Course"],
    response_model=List[CourseSchema],
    responses={
        200: {
            "model": List[CourseSchema]
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
async def get_active_courses(
    skip: int = 0, 
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseSchema]:
    """
    Просмотр всех неудалённых курсов
    """
    try:
        courses = await course_service.get_active_courses(db, skip=skip, limit=limit)

        logger.info(f"(Get active courses) Successfully retrieved {len(courses)} courses")
        return courses
    
    except Exception as e:
        logger.error(f"(Get active courses) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.get(
    "/{course_id}",
    tags=["Course"],
    response_model=CourseWithTasksSchema,
    responses={
        200: {
            "model": CourseWithTasksSchema
            },
        404: {
            "model": ErrorSchema, 
            "description": "Course not found"
            },
        500: {
            "model": ErrorSchema, 
            "description": "Internal server error"
            }
    }
)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> CourseWithTasksSchema:
    """
    Просмотр конкретного курса по ID с его задачами
    """
    try:
        course = await course_service.get_course_by_id(db, course_id)

        if not course:
            logger.warning(f"(Get course by ID) Course not found: {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"(Get course by ID) Course successfully found: {course.id}")
        return course

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"(Get course by ID) Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.put(
    "/{course_id}",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course updated successfully"
        },
        400: {
            "model": ErrorSchema,
            "description": "Validation error"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        404: {
            "model": ErrorSchema,
            "description": "Course not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    """
    Обвновление данных курса (только для администратора)
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Update course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Update course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")

        updated_course = await course_service.update_course(
            db = db,
            course_id=course_id,
            course_name=course_data.name,
            course_description=course_data.description,
            course_students_count=course_data.students_count,
            course_status=course_data.status
        )

        if not updated_course:
            raise HTTPException(
                status_code=404,
                detail=f"(Update course) Course with ID {course_id} not found"
            )
        
        """
        Поменять статус ошибки, если нужно будет
        """
        if updated_course == None:
            return MessageSchema(
                messageDigest=str(course_id),
                description="(Update course) No changes provided for the course"
            )

        return MessageSchema(
            messageDigest=str(course_id),
            description=f"(Update course) Course '{updated_course.name}' updated successfully"
        )

    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Update course) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Update course) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.put(
    "/{course_id}/delete",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course marked as deleted"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        404: {
            "model": ErrorSchema,
            "description": "Course not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def soft_delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    """
    Обновление статуса курса на удалённый (только для администратора)
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Delete status course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Delete status course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        deleted_course = await course_service.delete_status_course(db, course_id)

        if not deleted_course:
            raise HTTPException(status_code=404,detail=f"(Delete status course) Course with ID {course_id} not found")

        if deleted_course.status == "deleted":
            return MessageSchema(messageDigest=str(course_id), description=f"(Delete status course) Course with ID {course_id} was already marked as deleted")

        return MessageSchema(
            messageDigest=str(course_id),
            description=f"(Delete status course) Course with ID {course_id} marked as deleted"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Delete status course) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@course_router.delete(
    "/{course_id}/delete",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course deleted successfully"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Bad token"
        },
        404: {
            "model": ErrorSchema,
            "description": "Course not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def hard_delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(AuthService),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    """
    Удаление курса из базы данных (только для администратора)
    """
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Delete course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Delete course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        deleted_course = await course_service.delete_course(db, course_id)

        if not deleted_course:
            raise HTTPException(status_code=404, detail=f"(Delete course) Course with ID {course_id} not found")

        return MessageSchema(
            messageDigest=str(course_id),
            description=f"(Delete course) Course with ID {course_id} deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Delete course) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")