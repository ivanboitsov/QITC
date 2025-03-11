import logging
import traceback
import phonenumbers

from typing import List, Optional
from email_validator import validate_email, EmailNotValidError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.tables.application import Application

class ApplicationService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def _validate_phone_number(self, phone_number: str) -> str:
        """
        Валидация номера телефона
        """
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Uncorrect phone number")
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Phone number have to be interantional like +1234567890")
        

    async def _validate_email(self, email: str) -> str:
        """
        Валидация email
        """
        try:
            valid_email = validate_email(email)
            return valid_email.email
        except EmailNotValidError as e:
            raise ValueError(f"Uncorrect email: {e}")

    async def create_application(self,
                                 db: AsyncSession,
                                 user_name: str,
                                 phone_number: str,
                                 email: str,
                                 course_id: int):
        try:
            validated_phone_number = await self._validate_phone_number(phone_number)
            validated_email = await self._validate_email(email)

            application = Application(
                user_name = user_name,
                phone_number = validated_phone_number,
                email = validated_email,
                course_id = course_id
            )

            db.add(application)
            self.logger.info(f"Adding application: {application.__dict__}")
            await db.commit()
            self.logger.info("Commit successful")
            await db.refresh(application)

            self.logger.info(f"(Create application) Application with ID {application.id} was suuccessull created")
            return application
        
        except Exception as e:
            self.logger.error(f"(Create application) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise
    
    async def get_application_by_id(self, db: AsyncSession, _id: int) -> Optional[Application]:
        try:
            application = (await db.scalars(select(Application).where(Application.id == _id))).first()

            if not application:
                self.logger.info(f"(Get application by ID) Application with ID: {_id} not found")
                return None
            
            self.logger.info(f"(Get application by ID) Found application with ID: {_id}")
            return application
        except Exception as e:
            self.logger.error(f"(Get application by ID) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_applications(self, db: AsyncSession, skip = 0, limit = 50) -> List[Application]:
        try:
            applications = (await db.scalars(select(Application).offset(skip).limit(limit))).all()
            self.logger.info(f"(Get applications) Retrived {len(applications)} applications")
            return applications
        except Exception as e:
            self.logger.error(f"(Get applications) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise