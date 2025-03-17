from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from db.db_config import Base

class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    mark = Column(Integer, nullable=False)
    comment = Column(String)

    def __repr__(self):
        return f"<Group(id={self.id}, user_id={self.user_id}, task_id={self.task_id}, mark={self.mark}, comment='{self.comment}')>"