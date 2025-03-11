"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import PixelRectangle from "./pixel-rectangle";

interface Course {
  id: number;
  name: string;
  description: string;
  students_count: number;
  status: string;
}

export default function ApplicationFrom() {
  const [selectedCourse, setSelectedCourse] = useState("placeholder");
  const [selectedCourseId, setSelectedCourseId] = useState("");
  const [courses, setCourses] = useState<Course[]>([]);
  const [formData, setFormData] = useState({
    user_name: "",
    phone_number: "+7 ",
    email: "",
    course_id: "",
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get<Course[]>('/api/v1/qitc/course/active?skip=0&limit=10');
        setCourses(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке курсов:", error);
        setError("Ошибка при загрузке курсов");
      }
    };

    fetchCourses();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formattedPhone = formatPhone(e.target.value);
    setFormData({ ...formData, phone_number: formattedPhone });
  };

  const handleCourseChange = (value: string) => {
    const selected = courses.find((course) => course.id.toString() === value);
    if (selected) {
      setSelectedCourse(selected.name);
      setSelectedCourseId(selected.id.toString());
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  
    try {
      const cleanedPhoneNumber = formData.phone_number.replace(/\D/g, "");
  
      const internationalPhoneNumber = cleanedPhoneNumber.startsWith("7")
        ? `+${cleanedPhoneNumber}`
        : `+7${cleanedPhoneNumber}`;

      const payload = {
        user_name: formData.user_name,
        phone_number: internationalPhoneNumber,
        email: formData.email,
        course_id: Number(selectedCourseId),
      };
  
      const response = await axios.post('/api/v1/qitc/application', payload);
  
      if (response.status === 200) {
        alert("Заявка успешно отправлена!");
        setFormData({
          user_name: "",
          phone_number: "+7 ",
          email: "",
          course_id: "",
        });
        setSelectedCourse("placeholder");
      }
    } catch (error) {
      console.error("Ошибка при отправке заявки:", error);
      alert("Произошла ошибка при отправке заявки.");
    }
  };

  return (
    <section id="registration-form">
      {/* Верхняя надпись */}
      <h1 className="text-3xl text-center px-4 mb-5 mt-5">
        Место, где начинается великая история будущих лидеров технологий
      </h1>
      <div className="flex w-full h-[900px] items-center justify-center border-t">
        <div className="flex w-full h-full items-center max-w justify-between px-52 grid-background">
          <PixelRectangle>
            <div className="flex flex-col md:flex-row gap-6 p-12">
              <div className="flex-1 text-4xl text-white">
                <p>
                  Если у вас появилось желание записаться в кружок или остались вопросы — заполните заявку, и мы обязательно с вами свяжемся.
                </p>
              </div>
              <div className="flex-1">
                <form className="space-y-6" onSubmit={handleSubmit}>
                  <div>
                    <Label htmlFor="user_name" className="text-2xl">Имя</Label>
                    <Input
                      id="user_name"
                      name="user_name"
                      className="text-xl w-full h-14 px-4"
                      placeholder="Введите ваше имя"
                      style={{ fontSize: "1.875rem" }}
                      value={formData.user_name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="phone_number" className="text-2xl">Телефон</Label>
                    <Input
                      id="phone_number"
                      type="tel"
                      placeholder="+7 (___) ___-__-__"
                      className="h-14 px-4"
                      style={{ fontSize: "1.875rem" }}
                      value={formData.phone_number}
                      onChange={handlePhoneChange}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="email" className="text-2xl">Почта</Label>
                    <Input
                      id="email"
                      name="email" // Убедитесь, что name="email"
                      type="email"
                      className="h-14 px-4"
                      style={{ fontSize: "1.875rem" }}
                      placeholder="Введите вашу почту"
                      value={formData.email} // Значение берётся из состояния
                      onChange={handleInputChange} // Обработчик изменений
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="course_id" className="text-2xl">Кружок</Label>
                    <Select
                      onValueChange={handleCourseChange}
                      value={selectedCourse}
                    >
                      <SelectTrigger id="course_id" className="text-xl h-14" style={{ fontSize: "1.875rem" }}>
                        {selectedCourse !== "placeholder" ? selectedCourse : "Выберите кружок"}
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="placeholder" className="text-xl" disabled>
                          Выберите кружок
                        </SelectItem>
                        {courses.map((course) => (
                          <SelectItem key={course.id} value={course.id.toString()} className="text-xl">
                            {course.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <Button type="submit" className="w-full bg-black text-2xl h-12">
                    Отправить
                  </Button>
                </form>
              </div>
            </div>
          </PixelRectangle>
        </div>
      </div>
    </section>
  );
}

function formatPhone(value: string): string {
  const digits = value.replace(/\D/g, "");

  let formatted = "+7 ";
  if (digits.length > 1) formatted += `(${digits.slice(1, 4)}`;
  if (digits.length > 4) formatted += `) ${digits.slice(4, 7)}`;
  if (digits.length > 7) formatted += `-${digits.slice(7, 9)}`;
  if (digits.length > 9) formatted += `-${digits.slice(9, 11)}`;

  return formatted;
}