import logging

import traceback
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db

from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema
from services.applicatoin_service import ApplicationService
from models.schemas.application_schemas import ApplicationCreateSchema, ApplicationSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application_router = APIRouter(prefix="/application")

@application_router.post(
    "",
    tags=["Application"],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema,
            "description": "Application created successful"
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
async def create_application(
    application_data: ApplicationCreateSchema,
    application_service: ApplicationService = Depends(ApplicationService),
    db: AsyncSession = Depends(get_db)
    ) -> MessageSchema:
    try:
        application = await application_service.create_application(
            db=db,
            user_name=application_data.user_name,
            phone_number=application_data.phone_number,
            email=application_data.email,
            course_id=application_data.course_id
        )

        logger.info(f"(Create application) Application successfully created: {application.id}")
        return MessageSchema(
            messageDigest=str(application.id),
            description=f"(Create application) Application with ID {application.id} created succesfully"
        )
    
    except HTTPException:
        raise
    except ValueError as validate_error:
        logger.warning(f"(Create application) Validation error: {validate_error}")
        raise HTTPException(status_code=400, detail=str(validate_error))
    except Exception as e:
        logger.error(f"(Create application) Error: {e}")
        logger.error(traceback.format_exc()) 
        raise HTTPException(status_code=500, detail="Internal server error")


"""
Добавить просмотр только для авторизованного пользователя с правами администратора
"""
@application_router.get(
    "",
    tags=["Application"],
    response_model=List[ApplicationSchema],
    responses={
        200: {
            "model": List[ApplicationSchema]
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_applications(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    application_service: ApplicationService = Depends(ApplicationService)
    ) -> List[ApplicationSchema]:
    try:
        applications = await application_service.get_applications(db, skip=skip, limit=limit)
        logger.info(f"(Get applications) Successfully retrived {len(applications)} applications")
        return applications
    except Exception as e:
        logger.info(f"(Get applications) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

"""
Добавить просмотр только для авторизованного пользователя с правами администратора
"""
@application_router.get(
    "/{application_id}",
    tags=["Application"],
    response_model=ApplicationSchema,
    responses={
        200: {
            "model": ApplicationSchema
        },
        404: {
            "model": ErrorSchema, 
            "description": "Application not found"
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_application(
    application_id: int, 
    db: AsyncSession = Depends(get_db),
    application_service: ApplicationService = Depends(ApplicationService)
    ) -> ApplicationSchema:
    try:
        application = await application_service.get_application_by_id(db, application_id)

        if not application:
            logger.info(f"(Get application by id) Application with ID: {application_id} not found")
            raise HTTPException(status_code=404, detail="Application not found")
        
        logger.info(f"(Get application by id) Application successfully found: {application_id}")
        return application
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get application by id) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")