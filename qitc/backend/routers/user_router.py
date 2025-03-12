import traceback
import uuid
import logging

from typing import List
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from db.db_config import get_db
from config import oauth2_scheme

from services.auth_service import AuthService
from services.user_service import UserService

from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema
from models.schemas.access_token_schemas import AccessTokenSchema
from models.schemas.user_schemas import UserRegistrationSchema, UserProfileAdminSchema, UserLoginSchema, UserProfileSchema, UserSchema, UserProfileUpdateSchema, UserRoleStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/user")

@user_router.post(
    "/register",
    tags=["User"],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema,
            "description": "User register successful"
        },
        400:{
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def user_register(
    user_data: UserRegistrationSchema,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService)
    ) -> MessageSchema:
    try:

        user = await user_service.get_user_by_email(db, user_data.email)

        if user: 
            logger.warning(f"(User register) User with email '{user_data.email}' already exist")
            raise HTTPException(status_code=400, detail="User already exist")
        
        user = await user_service.create_user(
            db = db,
            name = user_data.name,
            email = user_data.email,
            password = user_data.password
        )

        logger.info(f"(User register) User successful register with ID {user.id}")
        return MessageSchema(
            messageDigest=str(user.id), 
            description="User register successfully"
        )

    except HTTPException:
        raise
    except ValueError as validation_error:
        logger.warning(f"(User registration) Validation error: {validation_error}")
        raise HTTPException(status_code=400, detail=str(validation_error))
    except Exception as e:
        logger.error(f"(User registration) Error {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.post(
    "/login",
    tags=["User"],
    response_model=AccessTokenSchema,
    responses={
        200:{
            "model": AccessTokenSchema,
            "description": "Login success"
        },
        400:{
            "model": ErrorSchema,
            "description": "Invalid input data"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def login(
    user_data: UserLoginSchema,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService),
    ) -> AccessTokenSchema:
    try:
        if not await user_service.verify_password(db, user_data.email, user_data.password):
            logger.warning(f"(Login) Failed login for user with email: {user_data.email}")
            raise HTTPException(status_code=400, detail="Invalid credentials")

        user = await user_service.get_user_by_email(db,  user_data.email)

        access_token = await auth_service.create_access_token(
            data={
                "sub": str(user.id),
                "role": str(user.role)
                }
        )

        logger.info(f"(Login) Login successful for user with ID: {user.id}")
        logger.info(f"(Login) User role: {user.role}")
        return AccessTokenSchema(access_token=access_token)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Registration) Error {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@user_router.post(
    "/logout",
    tags=["User"],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema,
            "description": "Success logout"
        },
        401:{
            "model": AccessTokenSchema,
            "description": "Unauthorized"
        },
        403:{
            "description": "Bad token"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def logout(
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    ) -> MessageSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Logout) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        await auth_service.revoke_access_token(db, access_token)
        logger.info(f"(Logout) Token was revoked: {access_token}")
        return MessageSchema(description="Token was successfully revoked")
    
    except JWTError as e:
        logger.warning(f"(Logout) Bad token {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Logout) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@user_router.get(
    "/profiles",
    tags=["User"],
    response_model=List[UserSchema],
    responses={
        200:{
            "model": List[UserSchema],
            "description": "Users profiles get successful"
        },
        401:{
            "model": ErrorSchema,
            "description": "Unauthorized"
        },
        403:{
            "model": ErrorSchema,
            "description": "Not allowed"
        },
        404: {
            "model": ErrorSchema,
            "description": "User not found"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_profiles(
    skip: int = 0,
    limit: int = 25,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
    ) -> List[UserSchema]:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get users profiles) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")
        
        token_data = await auth_service.get_data_from_access_token(access_token)
        role = token_data["role"]

        if role != "admin":
            logger.warning(f"(Get users profiles) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        users = await user_service.get_all_users(db, skip, limit)
        logger.info(f"(Get users profile) Successfully retrived {len(users)} user")
        return users
    
    except JWTError as e:
        logger.warning(f"(Get users profiles) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get users profiles) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.get(
    "/profile",
    tags=["User"],
    response_model=UserProfileSchema,
    responses={
        200:{
            "model": UserProfileSchema,
            "description": "User profile get successful"
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
            "description": "User not found"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def get_profile(
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
    ) -> UserProfileSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Get user profile) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        user = await user_service.get_user_by_id(db, token_data["sub"])
        logger.info(f"(Get user profile) Successful get profile with id: {user.id}")
        return user
    
    except JWTError as e:
        logger.warning(f"(Get user profile) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Get user profile) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.put(
    "/profile",
    tags=["User"],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema,
            "description": "User profile update successful"
        },
        400:{
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
        404: {
            "model": ErrorSchema,
            "description": "User not found"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def update_profile(
    user_data: UserProfileUpdateSchema,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
    ) -> MessageSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Update user profile) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        user = await user_service.get_user_by_id(db, token_data["sub"])

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"(Update user profile) User with ID {user.id} not found"
            )

        updated_user = await user_service.update_user(
            db,
            _id=user.id,
            name=user_data.name,
            email=user_data.email
        )  
        
        if updated_user == "no_changes":
            return MessageSchema(
                messageDigest=str(user.id),
                description="(Update user profile) No changes provided for the user"
            )

        return MessageSchema(
            messageDigest=str(user.id),
            description=f"(Update user profile) User '{user.name}' updated successfully"
        )
    except JWTError as e:
        logger.warning(f"(Update user profile) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Update user profile) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@user_router.put(
    "/profile/status",
    tags=["User"],
    response_model=MessageSchema,
    responses={
        200:{
            "model": MessageSchema,
            "description": "User status update successful"
        },
        400:{
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
        404: {
            "model": ErrorSchema,
            "description": "User not found"
        },
        500:{
            "model": ErrorSchema,
            "description": "Internal server error"
        }
    }
)
async def update_status_profile(
    user_data: UserProfileAdminSchema,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    auth_service: AuthService = Depends(AuthService)
    ) -> MessageSchema:
    try:
        if await auth_service.check_revoked(db, access_token):
            logger.warning(f"(Update user status) Token is revoked: {access_token}")
            raise HTTPException(status_code=403, detail="Token revoked")

        token_data = await auth_service.get_data_from_access_token(access_token)
        user = await user_service.get_user_by_id(db, token_data["sub"])
        role = token_data["role"]

        if user_data.role not in UserRoleStatus:
            logger.warning(f"(Update user status) Status {user_data.role} doesnt exist")
            raise HTTPException(status_code=400, detail=f"Task status '{user_data.role}' not exsist")

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"(Update user profile) User with ID {user.id} not found"
            )
        
        if role != "admin":
            logger.warning(f"(Update user status) Bad token: {access_token}")
            raise HTTPException(status_code=403, detail="Not allowed")
        
        update_user_status = await user_service.update_user_status(
            db = db, 
            _id = user_data.id, 
            role = user_data.role
        )

        if update_user_status == None:
            raise MessageSchema(
                messageDigest=str(user.id),
                description="(Update user status) No changes provided for the user"
            )

        return MessageSchema(
            messageDigest=str(user_data.id),
            description=f"(Update user status) User status updated successfully"
        )
    except JWTError as e:
        logger.warning(f"(Update user status) Bad token: {e}")
        raise HTTPException(status_code=403, detail="Bad token")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Update user status) Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")