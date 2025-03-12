import logging
import traceback
from jose import jwt
from jose import JWTError

from datetime import datetime, timedelta
from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tables.user import CRL
from config import oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger =  logging.getLogger(__name__)

        self.TOKEN_LIFETIME = int(ACCESS_TOKEN_EXPIRE_MINUTES)
        self.SECRET_KEY = str(JWT_SECRET_KEY)
        self.ALGORITHM = str(ALGORITHM)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)
    
    @staticmethod
    def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)
    
    """
    В токене хранится:
        1. Заголовок
            a. Тип токена
            b. Алгоритм подписи
        2. Payload (полезная загрузка)
            a. Словарь передаваемых данных
        3. Подпись
            a. Подпись создаваемая секретным ключом
    """
    async def create_access_token(self, data: dict) -> str:
        try:
            to_encode = data.copy()
            expire_delta = timedelta(minutes=self.TOKEN_LIFETIME)
            expire = datetime.now() + expire_delta
            to_encode.update({"exp": expire})
            encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

            self.logger.info(f"(Create access token) Successful created access token with payload: {data}")
            return encode_jwt
        except Exception as e:
            self.logger.error(f"(Create access token) Erorr creating access token: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_data_from_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            self.logger.info(f"(Get data from token) Successful get data: {payload}")
            return payload
        except JWTError as e:
            self.logger.warning(f"(Get data from token) Bad auth token {token}")
            raise
        except Exception as e:
            self.logger.error(f"(Get data from token) Error auth token: {e}")
            self.logger.error(traceback.format_exc())
            raise
    
    async def revoke_access_token(self, db: AsyncSession, token: str) -> None:
        try:
            crl_entry = CRL(token=token)
            db.add(crl_entry)
            await db.commit()
            await db.refresh(crl_entry)
            self.logger.info(f"(Revoke access token) Token revoked: {token}")
        except Exception as e:
            self.logger.error(f"(Revoke access token) Error token revoked: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise
    
    async def check_revoked(self, db: AsyncSession, token: str) -> bool:
        try:
            if (await db.scalars(select(CRL).where(CRL.token == token))).first():
                self.logger.info(f"(Check revoked access token) Token revoked: {token}")
                return True
            else:
                self.logger.warning(f"(Check revoked access token) Token not revoked: {token}")
                return False
        except Exception as e:
            self.logger.error(f"(Check revoked access token) Error revoking token: {e}")
            self.logger.error(traceback.format_exc())
            raise
    
    async def get_current_user_role(self, token: str) -> str:
        """
        Получает роль пользователя из токена.

        :param token: JWT-токен.
        :return: Роль пользователя.
        :raises ValueError: Если роль не найдена в токене.
        :raises JWTError: Если токен невалиден.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            role = payload.get("role")
            if role is None:
                raise ValueError("Role not found in token")
            return role
        except JWTError as e:
            self.logger.error(f"Invalid token: {e}")
            raise