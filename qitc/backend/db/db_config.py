from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()

# Создаём асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Функция для получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()