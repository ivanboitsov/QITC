import uuid
import logging
import traceback

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service import UserService

from models.tables.group import Group
from models.tables.user import User
from models.tables.course import Course
from models.tables.task import Task
from models.tables.journal import Journal

from models.schemas.group_schemas import GroupCourseWithStudentsSchema, GroupSchema
from models.schemas.user_schemas import UserProfileSchema

class GroupService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def add_student_to_course(self, db: AsyncSession, course_id: int, user_id: uuid) -> Optional[Group]:
        try:
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()

            if not user:
                self.logger.warning(f"(Add student to course) User {user_id} not found")
                return None
            
            if user.role != "student":
                self.logger.warning(f"(Add student to course) User {user_id} is not a student")
                return None

            existing_record = await db.execute(
                select(Group)
                .where(Group.course_id == course_id)
                .where(Group.user_id == user_id)
            )
            if existing_record.scalar():
                self.logger.warning(f"(Add student to course) Student {user_id} is already in course {course_id}")
                return None

            new_group = Group(course_id=course_id, user_id=user_id)
            db.add(new_group)

            tasks_result = await db.execute(select(Task.id).where(Task.course_id == course_id))
            tasks = tasks_result.scalars().all()

            new_jouranl_entries =[
                Journal(user_id = user_id, task_id=task_id, mark=0, comment="") for task_id in tasks
            ]
            db.add_all(new_jouranl_entries)

            await db.commit()
            await db.refresh(new_group)

            self.logger.info(f"(Add student to course) Student {user_id} added to course {course_id}")
            return new_group
        
        except Exception as e:
            self.logger.error(f"(Add student to course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise

    async def remove_student_from_course(self, db: AsyncSession, course_id: int, user_id: str) -> Optional[Group]:
        try:
            existing_record = await db.execute(
                select(Group)
                .where(Group.course_id == course_id)
                .where(Group.user_id == user_id)
            )
            group_entry = existing_record.scalar_one_or_none()

            if not group_entry:
                self.logger.warning(f"(Remove student from course) Student {user_id} is not in course {course_id}")
                return None

            await db.delete(group_entry)

            await db.execute(
                Journal.__table__.delete().where(
                    Journal.user_id == user_id,
                    Journal.task_id.in_(
                        select(Task.id).where(Task.course_id == course_id)
                    )
                )
            )

            await db.commit()

            self.logger.info(f"(Remove student from course) Student {user_id} removed from course {course_id} and journal updated")
            return Group

        except Exception as e:
            self.logger.error(f"(Remove student from course) Error: {e}")
            self.logger.error(traceback.format_exc())
            await db.rollback()
            raise

    async def get_students_by_course_id(self, db: AsyncSession, course_id: int) -> Optional[GroupCourseWithStudentsSchema]:
        try:
            query = (
                select(Course)
                .options(joinedload(Course.users))
                .filter(Course.id == course_id)
            )
            result = await db.execute(query)
            course = result.scalars().first()

            if not course:
                self.logger.warning(f"(Get students by course ID) Course with ID {course_id} not found")
                return None

            students = [
                UserProfileSchema(
                    name=user.name,
                    email=user.email,
                    role=user.role
                )
                for user in course.users
            ]

            course_schema = GroupCourseWithStudentsSchema(
                id=course.id,
                name=course.name,
                description=course.description,
                students_count=course.students_count,
                students=students
            )

            self.logger.info(f"(Get students by course ID) Course with ID {course_id} successfully found")
            return course_schema

        except Exception as e:
            self.logger.error(f"(Get students by course ID) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def get_all_groups(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[GroupCourseWithStudentsSchema]:
        try:
            result = await db.execute(
                select(Course)
                .options(joinedload(Course.users))
                .offset(skip)
                .limit(limit)
            )
            courses = result.unique().scalars().all()

            groups = []
            for course in courses:
                students = [
                    UserProfileSchema(
                        name=user.name,
                        email=user.email,
                        role=user.role
                    )
                    for user in course.users
                ]

                course_schema = GroupCourseWithStudentsSchema(
                    id=course.id,
                    name=course.name,
                    description=course.description,
                    students_count=course.students_count,
                    students=students
                )
                groups.append(course_schema)

            self.logger.info(f"(Get all groups) Retrieved {len(groups)} groups")
            return groups

        except Exception as e:
            self.logger.error(f"(Get all groups) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise