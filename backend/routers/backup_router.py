import os
import logging
import traceback

from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db
from config import oauth2_scheme

from services.auth_service import AuthService
from services.backup_service import BackupService
from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

backup_router = APIRouter(prefix="/backup", tags=["Backup"])

@backup_router.post(
        "/create",
        response_class=FileResponse,
        responses={
            200: {
                "model": "",
                "description": "Backup created successfully"
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
async def create_backup(
    backup_dir: str = "backups",
    #db: AsyncSession = Depends(get_db),
    #access_token: str = Depends(oauth2_scheme),
    #auth_service: AuthService = Depends(AuthService),
    backup_service: BackupService = Depends(BackupService)
    ):
    try:
        '''if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Create course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Create course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        '''
        backup_file = await backup_service.create_backup(backup_dir)
        logger.info(f"(Create backup) Backup successfully created")

        return FileResponse(backup_file, filename=os.path.basename(backup_file))
    
    except Exception as e:
        logger.error(f"(Create backup) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
    

@backup_router.post(
        "/restore",
        response_model=MessageSchema,
        responses={
            200: {
                "model": MessageSchema,
                "description": "Backup restored successfully"
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
async def restore_backup(
    backup_file: str,
    #db: AsyncSession = Depends(get_db),
    #access_token: str = Depends(oauth2_scheme),
    #auth_service: AuthService = Depends(AuthService),
    backup_service: BackupService = Depends(BackupService) 
    ):
    try:
        '''if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Create course) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Create course) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        '''
        await backup_service.restore_backup(backup_file)
        logger.info(f"(Restore backup) Backup successfully restored")

        return MessageSchema(
            messageDigest=str(backup_file),
            description=f"(Restore backup) Backup restored successuly"
        )
    except Exception as e:
        logger.error(f"(Create backup) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")