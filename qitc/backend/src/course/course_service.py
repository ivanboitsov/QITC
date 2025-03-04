import logging

from typing import List, Optional

from sqlalchemy.orm import Session
from course_models import Course

class CourseService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def get_course_by_id(self, db: Session, _id: int) -> Optional[Course]:
        try:
            course = db.query(Course).filter(Course.id == _id).first()

            if not course:
                self.logger.info(f"(Get course by ID) Course with ID {_id} not found")
                return None
            
            self.logger.info(f"(Get course by ID) Found course with ID {_id}")
            return course
        
        except Exception as e:
            self.logger.error(f"(Get course by ID) Error {e}")
            raise

    async def get_courses(self, db: Session, skip: int = 0, limit: int = 25) -> List[Course]:
        try:
            courses = db.query(Course).offset(skip).limit(limit).all()
            self.logger.info(f"(Get courses) Retrived {len(courses)} courses")
            return courses
        
        except Exception as e:
            self.logger.error(f"(Get courses) Error: {e}")
            raise
    

    async def create_course(self,
                            db: Session, 
                            name: str,
                            description: str,
                            students_count: int):
        try:
            course = Course(
                name = name,
                description = description,
                students_count = students_count
            )
            
            db.add(course)
            await db.commit()
            await db.refresh(course)

            self.logger.info(f"(Create course) Course with ID {course.id} was successfully created")
            return course

        except Exception as e:
            self.logger.error(f"(Create course) Error: {e}")
            await db.rollback()
            raise
    
    async def update_course(self,
                            db: Session,
                            course_id: int, 
                            course_name: str,
                            course_description: str,
                            course_students_count: int,
                            course_status: str):
        try:
            course = db.query(Course).filter(course.id == course_id).first()

            if not course:
                self.logger.info(f"(Update course) Course with id {course_id} not found")
                return None
            
            updates = {
                "name" : course_name,
                "description": course_description,
                "students_count": course_students_count,
                "status": course_status 
            }

            has_changes = any(
                getattr(course, key) != value for key, value in updates.items()
            )

            if has_changes:
                for key, value in updates.items():
                    setattr(course, key, value)
                
                await db.commit()
                await db.refresh(course)
                self.logger.info(f"(Update course) Course with ID {course_id} was update successfully")
            else:
                self.logger.info(f"(Update course) No updates for course with id {course_id}")
            return course

        except Exception as e:
            self.logger.error(f"(Update course) Error: {e}")
            await db.rollback()
            raise

    async def delete_course(self, db: Session, course_id: int) -> Optional[Course]:
        try:
            course = db.query(Course).filter(course.id == course_id).first()

            if not course:
                self.logger.info(f"(Delete course) Course with id {course_id} not found")
                return None
            
            if course.status != "deleted":
                course.status = "deleted"
                await db.commit()
                await db.refresh(course)
                self.logger.info(f"(Delete course) course with id {course_id} deleted successfully")
            else:
                self.logger.info(f"(Delete course) Course with id {course_id} was already delete")
            
            return course

        except Exception as e:
            self.logger.error(f"(Delete course) Error: {e}")
            await db.rollback()
            raise