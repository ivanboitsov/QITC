import logging

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db

from services.task_service import TaskService
from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema 
from models.schemas.task_schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema, TaskStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

task_router = APIRouter(prefix="/task")

"""
Добавить проверку на авторизацию и права администратора 
"""
@task_router.post(
    "",
    tags=["Task"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Task created successful"
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
async def create_task(
            task_data: TaskCreateSchema,
            db: AsyncSession = Depends(get_db),
            task_service: TaskService = Depends(TaskService)
    ) -> MessageSchema:
    try:

        task = await task_service.create_task(
            db = db, 
            name=task_data.name,
            description=task_data.description,
            course_id=task_data.course_id,
        )

        if not task:
            logger.info(f"(Create task) Course with ID {task_data.course_id} not found")
            raise HTTPException(status_code=400, detail="Invalid input data")

        logger.info(f"(Create task) Task successfully created: {task.id}")

        return MessageSchema(
            messageDigest=str(task.id),
            description=f"(Create task) Task '{task.name}' created successfully"
        )

    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Create task) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Create task) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""
Добавить проверку на авторизацию и права студента или учителя
"""
@task_router.get(
    "",
    tags=["Task"],
    response_model=List[TaskSchema],
    responses={
        200: {
            "model": List[TaskSchema]
        },
        500: {
            "model": ErrorSchema, 
            "description": "Internal server error"
        }
    }
)
async def get_tasks(
    skip: int = 0, 
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    task_service: TaskService = Depends(TaskService)
    ) -> List[TaskSchema]:
    try:
        tasks = await task_service.get_tasks(db, skip=skip, limit=limit)

        logger.info(f"(Get tasks) Successfully retrieved {len(tasks)} task")
        return tasks
    
    except Exception as e:
        logger.error(f"(Get tasks) Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )   
"""
Добавить проверку на авторизацию и права студента или учителя
"""
@task_router.get(
    "/{task_id}",
    tags=["Task"],
    response_model=TaskSchema,
    responses={
        200: {
            "model": TaskSchema
            },
        404: {
            "model": ErrorSchema, 
            "description": "Task not found"
            },
        500: {
            "model": ErrorSchema, 
            "description": "Internal server error"
            }
    }
)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    task_service: TaskService = Depends(TaskService)
    ) -> TaskSchema:
    try:
        task = await task_service.get_task_by_id(db, task_id)

        if not task:
            logger.info(f"(Get task by ID) Task not found: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"(Get task by ID) Task successfully found: {task.id}")
        return task

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"(Get task by ID) Error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

"""
Добавить проверку на авторизацию и права администратора 
"""
@task_router.put(
    "/{task_id}",
    tags=["Task"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Task updated successfully"
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        404: {
            "model": ErrorSchema,
            "description": "Task not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def update_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    db: AsyncSession = Depends(get_db),
    task_service: TaskService = Depends(TaskService)
    ) -> MessageSchema:
    try:
        updated_task = await task_service.update_task(
            db = db,
            task_id=task_id,
            task_name=task_data.name,
            task_description=task_data.description,
            task_course_id=task_data.course_id,
            task_status=task_data.status
        )

        if not updated_task:
            raise HTTPException(
                status_code=404,
                detail=f"(Update task) Task with ID {task_id} not found"
            )

        # Кастомизировать ошибку с INVALID INPUT DATA
        if updated_task == "no_changes":
            return MessageSchema(
                messageDigest=str(task_id),
                description="(Update task) No changes provided for the task"
            )

        return MessageSchema(
            messageDigest=str(task_id),
            description=f"(Update task) Task '{updated_task.name}' updated successfully"
        )

    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Update task) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Update task) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""
Добавить проверку на авторизацию и права студента или учителя 
"""
@task_router.put(
    "/{task_id}/status",
    tags=["Task"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Task status updated successfully"
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        404: {
            "model": ErrorSchema,
            "description": "Task not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def update_status_task(
    task_id: int,
    task_status: str,
    db: AsyncSession = Depends(get_db),
    task_service: TaskService = Depends(TaskService)
    ) -> MessageSchema:
    try:
        
        if task_status not in TaskStatus:
            logger.info(f"(Update status task) Status {task_status} doesnt exist")
            raise HTTPException(status_code=400, detail=f"Task status '{task_status}' not exsist")

        update_status_task = await task_service.update_task_status(
            db = db,
            task_id=task_id,
            status=task_status
        )

        if not update_status_task:
            raise HTTPException(
                status_code=404,
                detail=f"(Update status task) Task with id {task_id} not found"
            )
        
        # Кастомизировать ошибку с INVALID INPUT DATA
        if update_status_task == "no_changes":
            raise MessageSchema(
                messageDigest=str(task_id),
                description="(Update status task) No changes provided for the task"
            )

        return MessageSchema(
            messageDigest=str(task_id),
            description=f"(Update status task) Task '{update_status_task.name}' updated successfully"
        )
    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(Update status task) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(Update status task) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

"""
Добавить проверку на авторизацию и права администратора 
"""
@task_router.put(
    "/{task_id}/delete",
    tags=["Task"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Task marked as deleted"
        },
        404: {
            "model": ErrorSchema,
            "description": "Task not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def soft_delete_task(
        task_id: int,
        db: AsyncSession = Depends(get_db),
        task_service: TaskService = Depends(TaskService)
    ) -> MessageSchema:
    try:
        deleted_task = await task_service.delete_status_task(db, task_id)

        if not deleted_task:
            raise HTTPException(status_code=404,detail=f"(Delete status task) Task with ID {task_id} not found")
        
        
        if deleted_task == "already_deleted":
            return MessageSchema(messageDigest=str(task_id), description=f"(Delete status task) Task with ID {task_id} was already marked as deleted")
        
        return MessageSchema(
            messageDigest=str(task_id),
            description=f"(Delete status task) Task with ID {task_id} marked as deleted"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Delete status task) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
"""
Добавить проверку на авторизацию и права администратора 
"""
@task_router.delete(
    "/{task_id}/delete",
    tags=["Task"],
    response_model=MessageSchema,
    responses={
        200: {
            "model": MessageSchema,
            "description": "Task deleted successfully"
        },
        404: {
            "model": ErrorSchema,
            "description": "Task not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def hard_delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    task_service: TaskService = Depends(TaskService)
    ) -> MessageSchema:
    try:
        deleted_task = await task_service.delete_task(db, task_id)

        if not deleted_task:
            raise HTTPException(status_code=404, detail=f"(Delete task) Task with ID {task_id} not found")

        return MessageSchema(
            messageDigest=str(task_id),
            description=f"(Delete task) Task with ID {task_id} deleted successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Delete task) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")