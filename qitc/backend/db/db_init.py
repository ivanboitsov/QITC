import logging
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def db_init():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("(Init database) Database initialized successfully")
    except Exception as e:
        logger.fatal(f"(Init database) Error: {e}")
        raise