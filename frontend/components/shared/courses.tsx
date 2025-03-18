'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import axios from 'axios';

interface Course {
  id: number;
  name: string;
  description: string;
  students_count: number;
  status: string;
}

const Courses = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get<Course[]>('/api/v1/qitc/course/active?skip=0&limit=10');
        setCourses(response.data);
        setError(null);
      } 
      catch (error) {
        setError('Ошибка при загрузке курсов');
        console.error(error);
      } 
      finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>Ошибка: {error}</div>;
  }

  return (
    <section id="courses">
      <div className="courses-container">
        <h2 className="text-3xl mb-5 mt-5 text-center">Познакомьте ребенка с профессиями будущего уже сейчас</h2>

        <div className="grid grid-cols-3 gap-5">
          {courses.map((course) => (
            <div key={course.id} className="cassette-wrapper">
              <div className="cassette-container">
                <Image src="/audio.png" alt="Cassette" className="cassette-image" width={512} height={512}/>
                <div className="course-name">{course.name}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Courses;