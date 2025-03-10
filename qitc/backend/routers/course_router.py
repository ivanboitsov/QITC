import logging
import traceback

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db

from services.course_service import CourseService
from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema 
from models.schemas.course_schemas import CourseWithTasksSchema, CourseCreateSchema, CourseSchema, CourseUpdateSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

course_router = APIRouter(prefix="/course")

"""
Добавить проверку на авторизацию и права администратора 
"""
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
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def create_course(
    course_data: CourseCreateSchema,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    try:

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
        500: {
            "model": ErrorSchema, 
            "description": "Internal server error"
            }
    }
)
async def get_courses(
    skip: int = 0, 
    limit: int = 25,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseSchema]:
    try:
        courses = await course_service.get_courses(db, skip=skip, limit=limit)

        logger.info(f"(Get courses) Successfully retrieved {len(courses)} courses")
        return courses
    
    except Exception as e:
        logger.error(f"(Get courses) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
    
@course_router.get(
    "/active",
    tags=["Course"],
    response_model=List[CourseSchema],
    responses={
        200: {
            "model": List[CourseSchema]
            },
        500: {
            "model": ErrorSchema, 
            "description": "Internal server error"
            }
    }
)
async def get_not_deleted_courses(
    skip: int = 0, 
    limit: int = 25,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseSchema]:
    try:
        courses = await course_service.get_not_deleted_courses(db, skip=skip, limit=limit)

        logger.info(f"(Get not deleted courses) Successfully retrieved {len(courses)} courses")
        return courses
    
    except Exception as e:
        logger.error(f"(Get not deleted courses) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")


@course_router.get(
    "/with-tasks",
    tags=["Course"],
    response_model=List[CourseWithTasksSchema],
    responses={
        200: {
            "model": List[CourseWithTasksSchema],
            "description": "List of courses with tasks"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_courses_with_tasks(
    skip: int = 0,
    limit: int = 25,
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> List[CourseWithTasksSchema]:
    try:
        courses = await course_service.get_courses_with_tasks(db, skip=skip, limit=limit)

        logger.info(f"(Get courses with tasks) Successfully retrieved {len(courses)} courses")
        return courses

    except Exception as e:
        logger.error(f"(Get courses with tasks) Error: {e}", exc_info=True)
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
    try:
        course = await course_service.get_course_by_id(db, course_id)

        if not course:
            logger.info(f"(Get course by ID) Course not found: {course_id}")
            raise HTTPException(status_code=404, detail="Course not found")

        logger.info(f"(Get course by ID) Course successfully found: {course.id}")
        return course

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"(Get course by ID) Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

"""
Добавить проверку на авторизацию и права администратора 
"""
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
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    try:
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
        if updated_course == "no_changes":
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


"""
Добавить проверку на авторизацию и права администратора 
"""
@course_router.put(
    "/{course_id}/soft-delete",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course marked as deleted"
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
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    try:
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

"""
Добавить проверку на авторизацию и права администратора 
"""
'''
@course_router.delete(
    "/{course_id}",
    tags=["Course"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Course deleted successfully"
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
    course_service: CourseService = Depends(CourseService)
    ) -> MessageSchema:
    try:
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
'''