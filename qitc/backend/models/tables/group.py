from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from db.db_config import Base

class Group(Base):
    __tablename__ = 'group'

    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), primary_key=True)

    def __repr__(self):
        return f"<Group(user_id={self.user_id}, course_id={self.course_id})>"