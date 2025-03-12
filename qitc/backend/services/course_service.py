import logging
import traceback

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from models.tables.course import Course
from models.tables.task import Task

class CourseService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def get_course_by_id(self, db: AsyncSession, _id: int) -> Optional[Course]:
        try:
            course = (
                await db.scalars(
                    select(Course)
                    .where(Course.id == _id)
                    .options(selectinload(Course.tasks))
                    )
                ).first()

            if not course:
                self.logger.warning(f"(Get course by ID) Course with ID {_id} not found")
                return None
            
            self.logger.info(f"(Get course by ID) Found course with ID {_id}")
            return course
        
        except Exception as e:
            self.logger.error(f"(Get course by ID) Error {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_courses(self, db: AsyncSession, skip: int = 0, limit: int = 25) -> List[Course]:
        try:
            courses = (
                await db.execute(
                    select(Course)
                    .offset(skip)
                    .limit(limit)
                    )
                ).scalars().all()
            self.logger.info(f"(Get courses) Retrieved {len(courses)} courses")
            return courses
        
        except Exception as e:
            self.logger.error(f"(Get courses) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise
    
    async def get_active_courses(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Course]:
        try:
            courses = (
                await db.execute(
                    select(Course)
                    .where(Course.status != "deleted" or Course.status != "closed")
                    .offset(skip)
                    .limit(limit)
                    )
                ).scalars().all()
            self.logger.info(f"(Get not deleted courses) Retrieved {len(courses)} courses")
            return courses
        
        except Exception as e:
            self.logger.error(f"(Get not deleted courses) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    # Функция для получения полного списка курсов с его задачами
    async def get_courses_with_tasks(self, db: AsyncSession, skip: int = 0, limit: int = 5) -> List[Course]:
        try:
            courses = (
                await db.execute(
                    select(Course)
                    .options(selectinload(Course.tasks))
                    .offset(skip)
                    .limit(limit)
                    )
                ).scalars().all()
            
            for course in courses:
                if not course.tasks:
                    course.tasks = (await db.scalars(select(Task).where(Task.course_id == course.id))).all()

            self.logger.info(f"(Get courses with tasks) Retrieved {len(courses)} courses")
            return courses

        except Exception as e:
            self.logger.error(f"(Get courses with tasks) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def create_course(self,
                            db: AsyncSession, 
                            name: str,
                            description: str,
                            students_count: int
                            ) -> Course:
        try:
            existing_course = (await db.scalars(select(Course).where(Course.name == name))).first()
            if existing_course:
                raise ValueError("Course with this name already exists")

            course = Course(
                name = name,
                description = description,
                students_count = students_count
            )
            
            db.add(course)
            await db.commit()
            await db.refresh(course)

            self.logger.info(f"(Create course) Course with ID {course.id} was successfully created: {course.name}")
            return course

        except Exception as e:
            self.logger.error(f"(Create course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise
    
    async def update_course(self,
                            db: AsyncSession,
                            course_id: int, 
                            course_name: str,
                            course_description: str,
                            course_students_count: int,
                            course_status: str) -> Optional[Course]:
        try:
            course = (await db.scalars(select(Course).where(Course.id == course_id))).first()

            if not course:
                self.logger.warning(f"(Update course) Course with id {course_id} not found")
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
                self.logger.warning(f"(Update course) No updates for course with id {course_id}")
                return None
            return course

        except Exception as e:
            self.logger.error(f"(Update course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise

    async def delete_status_course(self, db: AsyncSession, course_id: int) -> Optional[Course]:
        try:
            course = (await db.scalars(select(Course).where(Course.id == course_id))).first()

            if not course:
                self.logger.warning(f"(Delete status course) Course with id {course_id} not found")
                return None
            
            if course.status != "deleted":
                course.status = "deleted"
                await db.commit()
                await db.refresh(course)
                self.logger.info(f"(Delete status course) course with id {course_id} deleted successfully")
            else:
                self.logger.warning(f"(Delete status course) Course with id {course_id} was already delete")
                return None
            
            return course

        except Exception as e:
            self.logger.error(f"(Delete status course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise

    async def delete_course(self, db: AsyncSession, course_id: int) -> Optional[Course]:
        try:
            course = (await db.scalars(select(Course).where(Course.id == course_id))).first()

            if not course:
                self.logger.warning(f"(Delete course) Course with id {course_id} not found")
                return None

            await db.delete(course)
            await db.commit()

            self.logger.info(f"(Delete course) Course with id {course_id} was successfully deleted")
            return course

        except Exception as e:
            self.logger.error(f"(Delete course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise