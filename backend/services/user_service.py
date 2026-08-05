import uuid
import logging
import traceback

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from email_validator import validate_email, EmailNotValidError
from config import oauth2_scheme, MIN_PASSWORD_LENGTH

from models.tables.user import User
from services.auth_service import AuthService


class UserService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.PASSWORD_LENGTH = int(MIN_PASSWORD_LENGTH)

    async def _validate_email(self, email: str) -> str:
        """
        Валидация email
        """
        try:
            valid_email = validate_email(email)
            return valid_email.email
        except EmailNotValidError as e:
            raise ValueError(f"Uncorrect email: {e}")

    async def get_user_by_id(self, db: AsyncSession, _id: uuid) -> Optional[User]:
        try:
            user = (await db.scalars(select(User).where(User.id == _id))).first()

            if not user:
                self.logger.info(f"(Get user by ID) User with id {_id} no found")
                return None
            
            self.logger.info(f"(Get user by ID) User successfully found with ID {user.id}")
            return user
        
        except Exception as e:
            self.logger.error(f"(Get user by ID) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        try:
            user = (await db.scalars(select(User).where(User.email == email))).first()

            if not user:
                self.logger.info(f"(Get user by email) User with email {email} no found")
                return None
            
            self.logger.info(f"(Get user by email) User successfully found")
            return user
        
        except Exception as e:
            self.logger.error(f"(Get user by email) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_all_users(self, db: AsyncSession, skip: int = 0, limit: int = 25) -> List[User]:
        try:
            users = (
                await db.scalars(
                    select(User)
                    .offset(skip)
                    .limit(limit)
                )
            ).all()
            self.logger.info(f"(Get all users) Retrieved {len(users)} users")
            return users
        
        except Exception as e:
            self.logger.error(f"(Get all users) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def verify_password(self, db: AsyncSession, email: str, password: str) -> bool:
        try:
            user = await self.get_user_by_email(db, email)

            if not user:
                self.logger.info(f"(Password verify) No same user found with email '{email}'")
                return False

            if AuthService.verify_hashed_password(password, user.password):
                self.logger.info(f"(Password verify) Success: {email}")
                return True
            else:
                self.logger.info(f"(Password verify) Failure: {email}")
                return False

        except Exception as e:
            self.logger.error(f"(Password verify) Error: {email}")
            self.logger.error(traceback.format_exc())
            raise

    async def create_user(self, 
                          db: AsyncSession, 
                          name: str,  
                          email: str, 
                          password: str):
        try:
            if len(password) < self.PASSWORD_LENGTH:
                raise ValueError("Password need to contain more then 8 letters")

            hashed_password = AuthService.get_hashed_password(password)

            validated_email = await self._validate_email(email)

            user = User(
                name = name,
                email = validated_email,
                password = hashed_password
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)
            self.logger.info(f"(Creating user) User successfully created: {user.id}")
            return user
        
        except Exception as e:
            self.logger.error(f"(Creating user) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise
    

    async def update_user(self, 
                          db: AsyncSession, 
                          _id: uuid, 
                          name: str, 
                          email: str
                          ) -> Optional[User]:
        try:
            user = await self.get_user_by_id(db, _id)

            if not user:
                self.logger.info(f"(Update user) User with ID: {_id} not found")
                return None
            
            updates = {
                "name": name,
                "email": email,
            }

            has_changes = any(
                getattr(user, key) != value for key, value in updates.items()
            )

            if has_changes:
                for key, value in updates.items():
                    setattr(user, key, value)

                await db.commit()
                await db.refresh(user)
                self.logger.info(f"(Update user) User with ID {user.id} succesfully update")
            else:
                self.logger.info(f"(Update user) No updates for user with ID {user.id}")
                return "no_changes"
            return user
        
        except Exception as e:
            self.logger.error(f"(Updating user) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise
    
    async def update_user_status(self, 
                          db: AsyncSession, 
                          _id: uuid, 
                          role: str) -> Optional[User]:
        try:
            user = await self.get_user_by_id(db, _id)

            if not user:
                self.logger.info(f"(Update user status) User with ID: {_id} not found")
                return None

            if user.role != role:
                user.role = role

                await db.commit()
                await db.refresh(user)
                self.logger.info(f"(Update user status) User with ID {user.id} succesfully update")
            else:
                self.logger.info(f"(Update user status) No updates for user with ID {user.id}")
                return None
            return user
        
        except Exception as e:
            self.logger.error(f"(Updating user status) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise