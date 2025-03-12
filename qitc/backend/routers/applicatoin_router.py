import logging

import traceback
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db
from config import oauth2_scheme

from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema
from services.auth_service import AuthService
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


@application_router.get(
    "",
    tags=["Application"],
    response_model=List[ApplicationSchema],
    responses={
        200: {
            "model": List[ApplicationSchema]
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
async def get_applications(
    skip: int = 0,
    limit: int = 50,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    application_service: ApplicationService = Depends(ApplicationService),
    auth_service: AuthService = Depends(AuthService)
    ) -> List[ApplicationSchema]:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get applications) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get applications) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")

        applications = await application_service.get_applications(db, skip=skip, limit=limit)
        logger.info(f"(Get applications) Successfully retrived {len(applications)} applications")
        return applications
    except Exception as e:
        logger.error(f"(Get applications) Error: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")


@application_router.get(
    "/{application_id}",
    tags=["Application"],
    response_model=ApplicationSchema,
    responses={
        200: {
            "model": ApplicationSchema
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
    access_token: str = Depends(oauth2_scheme),
    application_service: ApplicationService = Depends(ApplicationService),
    auth_service: AuthService = Depends(AuthService)
    ) -> ApplicationSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get application by id) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get application by id) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")

        application = await application_service.get_application_by_id(db, application_id)

        if not application:
            logger.warning(f"(Get application by id) Application with ID: {application_id} not found")
            raise HTTPException(status_code=404, detail="Application not found")
        
        logger.info(f"(Get application by id) Application successfully found: {application_id}")
        return application
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get application by id) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")