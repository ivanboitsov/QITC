from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from db.db_config import Base
from models.tables.journal import Journal

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum('closed', 'inProcess', 'done', 'deleted', name="task_status"), default='closed', nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)

    users = relationship("User", secondary=Journal.__table__, back_populates="tasks", lazy='select')
    course = relationship("Course", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', description='{self.description}', status='{self.status}', course_id={self.course_id})>"