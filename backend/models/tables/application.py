from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from db.db_config import Base

class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)
    status = Column(Enum('readed', 'new', name='application_status'), default='new', nullable=False)
    application_date = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Application(id={self.id}, user_name='{self.user_name}', phone_number='{self.phone_number}', email='{self.email}' course_id={self.course_id}, status='{self.status}', application_date='{self.application_date}')>"