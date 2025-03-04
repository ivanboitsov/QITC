import logging

from typing import List, Optional

from sqlalchemy.orm import Session
from task_models import Task

class TaskService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    # Функции для всех пользователей
    async def get_task_by_id(self, db: Session, _id: int) -> Optional[Task]:
        try:
            task = db.query(Task).filter(Task.id == _id).first()

            if task:
                self.logger.info(f"(Get task by ID) Found task with ID {_id}")
                return task
            else:
                self.logger.info(f"(Get task by ID) Task with ID {_id} not found")
                return None
            
        except Exception as e:
            self.logger.error(f"(Get task by ID) Error {e}")
            raise

    async def get_taks_by_course_id(self, db: Session, course_id: int) -> List[Task]:
        try:
            tasks = db.query(Task).filter(Task.course_id == course_id).all()
            self.logger.info(f"(Get tasks by course id) Retrived {len(tasks)} task from the course with id {course_id}")
            return tasks
        except Exception as e:
            self.logger.error(f"(Get tasks by course id) Error: {e}")
            raise

    async def get_tasks(self, db: Session, skip: int = 0, limit: int = 50) -> List[Task]:
        try:
            tasks = db.query(Task).offset(skip).limit(limit).all()
            self.logger.info(f"(Get tasks) Retrived {len(tasks)} tasks")
            return tasks
        
        except Exception as e:
            self.logger.error(f"(Get tasks) Error: {e}")
            raise
    
    async def update_task_status(self, db: Session, task_id: int, status: str) -> Optional[Task]:
        try:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                self.logger.info(f"(Update task status) Task with id {task_id} not found")
                return None

            if task.status != status:
                task.status = status
                await db.commit()
                await db.refresh(task)
                self.logger.info(f"(Update task status) Status on task with id {task_id} was update successfull")
            else:
                self.logger.info(f"(Update task status) Same status on task with id {task_id}")
            return task
        
        except Exception as e:
            self.logger.error(f"(Update task status) Error: {e}")
            await db.rollback()
            raise

    # Функции для пользователей с правами администратора
    async def create_task(self, 
                          db: Session,
                          name: str,
                          description: str,
                          course_id: int):
        try:
            task = Task(
                name = name,
                description = description,
                course_id = course_id
            )

            db.add(task)
            await db.commit()
            await db.refresh(task)

            self.logger.info(f"(Create task) Task with ID {task.id} was successfull created")
            return task
        
        except Exception as e:
            self.logger.error(f"(Create task) Error: {e}")
            await db.rollback()
            raise

    async def update_task(self, 
                          db: Session,
                          task_id: int, 
                          task_name: str,
                          task_description: str,
                          task_status: str,
                          task_course_id: int) -> Optional[Task]:
        try:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                self.logger.info(f"(Update task) Task with id {task_id} not found")
                return None
            
            updates = {
                "name": task_name,
                "description": task_description,
                "status": task_status,
                "course_id": task_course_id
            }

            has_changes = any(
                getattr(task, key) != value for key, value in updates.items()
            )

            if has_changes:
                for key, value in updates.items():
                    setattr(task, key, value)

                await db.commit()
                await db.refresh(task)
                self.logger.info(f"(Update task) Task with id {task_id} was update successfully")
            else:
                self.logger.info(f"(Update task) No updates for task with id {task_id}")
            return task
        
        except Exception as e:
            self.logger.error(f"(Update task) Error: {e}")
            await db.rollback()
            raise

    async def delete_task(self, db: Session, task_id: int) -> Optional[Task]:
        try:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                self.logger.info(f"(Delete task) Task with id {task_id} not found")
                return None

            if task.status != "deleted":
                task.status = "deleted"
                await db.commit()
                await db.refresh(task)
                self.logger.info(f"(Delete task) Task with id {task_id} deleted successfully")
            else:
                self.logger.info(f"(Delete task) Task with id {task_id} was already delete")
            return task
        
        except Exception as e:
            self.logger.error(f"(Delete task) Error: {e}")
            await db.rollback()
            raise