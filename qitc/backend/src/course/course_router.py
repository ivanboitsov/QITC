from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from db.db_config import get_db

from course_service import CourseService
from course_dto import CourseResponse

course_router = APIRouter()

@course_router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course_service = CourseService()
    course = await course_service.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.get("/courses/", response_model=List[CourseResponse])
async def get_courses(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    course_service = CourseService()
    courses = await course_service.get_courses(db, skip=skip, limit=limit)
    return courses

@course_router.post("/courses/", response_model=CourseResponse)
async def create_course(name: str, description: str, students_count: int, db: Session = Depends(get_db)):
    course_service = CourseService()
    course = await course_service.create_course(db, name=name, description=description, students_count=students_count)
    return course

@course_router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    name: str,
    description: str,
    students_count: int,
    status: str,
    db: Session = Depends(get_db)
):
    course_service = CourseService()
    course = await course_service.update_course(
        db,
        course_id=course_id,
        course_name=name,
        course_description=description,
        course_students_count=students_count,
        course_status=status
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@course_router.delete("/courses/{course_id}", response_model=CourseResponse)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course_service = CourseService()
    course = await course_service.delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course