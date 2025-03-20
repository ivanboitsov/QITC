import uuid
import logging
import traceback

from fastapi import Request
from db.db_config import get_db
from starlette.config import Config

from services.auth_service import oauth

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from authlib.integrations.starlette_client import OAuthError

from services.auth_service import AuthService
from services.user_service import UserService

from models.schemas.error_schemas import ErrorSchema
from models.schemas.message_schemas import MessageSchema
from models.schemas.access_token_schemas import AccessTokenSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.get(
    "/yandex",
    tags=["Auth"],
    responses={
        302: {
            "description": "Redirect to Yandex OAuth page",
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error",
        },
    },
)
async def auth_yandex(request: Request):
    """
    Перенаправляет пользователя на страницу авторизации Yandex
    """
    try:
        redirect_uri = "http://localhost:8000/api/v1/qitc/auth/yandex/callback"
        return await oauth.yandex.authorize_redirect(request, redirect_uri)
    
    except Exception as e:
        logger.error(f"(Yandex Auth) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get(
    "/yandex/callback",
    tags=["Auth"],
    response_model=AccessTokenSchema,
    responses={
        200: {
            "model": AccessTokenSchema,
            "description": "Yandex OAuth successful, returns access token",
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid OAuth response or missing email",
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error",
        },
    },
)
async def auth_yandex_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    user_service: UserService = Depends(UserService),
) -> AccessTokenSchema:
    """
    Обрабатывает callback от Yandex OAuth и возвращает JWT токен
    """
    try:
        token = await oauth.yandex.authorize_access_token(request)
        userinfo = await oauth.yandex.get('https://login.yandex.ru/info', token=token)
        userinfo = userinfo.json()

        email = userinfo.get('default_email')
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Yandex")

        user = await user_service.get_user_by_email(db, email)
        if not user:
            user = await user_service.create_user(
                db=db,
                name=userinfo.get('real_name', 'Unknown'),
                email=email,
                password=str(uuid.uuid4()),
            )

        access_token = await auth_service.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        logger.info(f"(Yandex Auth) Successful login for user with ID: {user.id}")
        return AccessTokenSchema(access_token=access_token)

    except OAuthError as e:
        logger.error(f"(Yandex Auth) OAuthError: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(Yandex Auth) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get(
    "/vk",
    tags=["Auth"],
    responses={
        302: {
            "description": "Redirect to VK OAuth page",
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error",
        },
    },
)
async def auth_vk(request: Request):
    """
    Перенаправляет пользователя на страницу авторизации VK
    """
    try:
        redirect_uri = "http://localhost:8000/api/v1/qitc/auth/vk/callback"
        return await oauth.vk.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logger.error(f"(VK Auth) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

@auth_router.get(
    "/vk/callback",
    tags=["Auth"],
    response_model=AccessTokenSchema,
    responses={
        200: {
            "model": AccessTokenSchema,
            "description": "VK OAuth successful, returns access token",
        },
        400: {
            "model": ErrorSchema,
            "description": "Invalid OAuth response or missing email",
        },
        500: {
            "model": ErrorSchema,
            "description": "Internal server error",
        },
    },
)
async def auth_vk_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(AuthService),
    user_service: UserService = Depends(UserService),
) -> AccessTokenSchema:
    """
    Обрабатывает callback от VK OAuth и возвращает JWT токен
    """
    try:
        token = await oauth.vk.authorize_access_token(request)
        userinfo = await oauth.vk.get(
            'https://api.vk.com/method/users.get',
            token=token,
            params={'v': '5.131', 'fields': 'email,first_name,last_name'},
        )
        userinfo = userinfo.json()

        email = userinfo['response'][0].get('email')
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by VK")

        user = await user_service.get_user_by_email(db, email)
        if not user:
            user = await user_service.create_user(
                db=db,
                name=f"{userinfo['response'][0]['first_name']} {userinfo['response'][0]['last_name']}",
                email=email,
                password=str(uuid.uuid4()),
            )

        access_token = await auth_service.create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )
        logger.info(f"(VK Auth) Successful login for user with ID: {user.id}")
        return AccessTokenSchema(access_token=access_token)

    except OAuthError as e:
        logger.error(f"(VK Auth) OAuthError: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"(VK Auth) Error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")