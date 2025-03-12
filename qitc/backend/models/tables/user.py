import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from db.db_init import Base
from models.tables.journal import Journal
from models.tables.group import Group

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String(254), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(Enum('user', 'student', 'admin', name='user_role'), nullable=False, default='user')
    user_date_auth = Column(DateTime, server_default=func.now())

    courses = relationship("Course", secondary=Group.__table__, back_populates="users", lazy='select')
    tasks = relationship("Task", secondary=Journal.__table__, back_populates="users", lazy='select')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}', role='{self.role}', user_date_auth='{self.user_date_auth}')>"

# Отозванные сертификаты
class CRL(Base):
    __tablename__ = "crl"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    token = Column(String, index=True, nullable=False)

    def __repr__(self):
        return f"<crl(id={self.id}, token='{self.token}')>"