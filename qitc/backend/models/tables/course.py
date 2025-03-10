from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.db_config import Base

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    students_count = Column(Integer, default=0)
    status = Column(Enum('active', 'closed', 'deleted', name='course_status'), default='active', nullable=False)

    # Связь с заданиями (tasks)
    tasks = relationship("Task", back_populates="course", cascade="all, delete-orphan", lazy='select')

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}', description='{self.description}', students_count={self.students_count}, status='{self.status}')>"