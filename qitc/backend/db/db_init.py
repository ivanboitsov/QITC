import logging

from db_config import SessionLocal, Base, engine

from src.course.course_models import Course
from src.task.task_models import Task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def db_init():
    db = SessionLocal()

    try:
        Base.metadata.create_all(bind=engine, tables = [Course.__table__,
                                                        Task.__table__])
        db.commit()
        logger.info("(Init database) Database initialized successfully")
    except Exception as e:
        db.rollback()
        logger.fatal(f"(Init database) Initializing database: {e} ")
    finally:
        db.close()