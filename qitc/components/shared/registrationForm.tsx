"use client";
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import { Label } from "@/components/ui/label";

export default function RegistrationForm() {
    const [selectedCourse, setSelectedCourse] = React.useState("placeholder");

  return (
    <section id="registration-form">
    {/* Верхняя надпись */}
    <h1 className="text-4xl text-center px-4 mb-8">
      Место, где начинается великая история будущих лидеров технологий
    </h1>
    <div className="flex w-full h-[900px] items-center justify-center border-t fixed-width-container">
      <div className="flex w-full h-full items-center max-w justify-between px-52 grid-background">
        <div className="flex flex-col md:flex-row gap-6 p-12 bg-[#03C9A1] rounded-lg shadow-md">
          <div className="flex-1 text-5xl text-white">
            <p>
              Если у вас появилось желание записаться в кружок или остались вопросы — заполните заявку, и мы обязательно с вами свяжемся.
            </p>
          </div>
          <div className="flex-1">
            <form className="space-y-6">
              <div>
                <Label htmlFor="fio" className="text-3xl">Имя</Label>
                <Input 
                    id="fio" 
                    name="fio" 
                    className="text-xl w-full h-14 px-4" 
                    placeholder="Введите ваше имя" 
                    style={{fontSize: "1.875rem"}}
                />
              </div>
              <div>
                <Label htmlFor="phone" className="text-3xl">Телефон</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="+7 (___) ___-__-__"
                  className="h-14 px-4"
                  style={{fontSize: "1.875rem"}}
                  required
                  defaultValue="+7 "
                  onInput={(e) => {
                    let input = e.target as HTMLInputElement;
                    input.value = formatPhone(input.value);
                  }}
                />
              </div>
              <div>
                <Label htmlFor="email" className="text-3xl">Почта</Label>
                <Input
                  id="email"
                  type="email"
                  className="h-14 px-4"
                  style={{fontSize: "1.875rem"}}
                  placeholder="Введите вашу почту"
                  required
                />
              </div>
              <div>
                <Label htmlFor="course" className="text-3xl">Кружок</Label>
                <Select
                    onValueChange={(value) => setSelectedCourse(value)}
                    value={selectedCourse}>
                    <SelectTrigger id="course" className="text-xl h-14" style={{fontSize: "1.875rem"}}>
                    {selectedCourse !== "placeholder" ? selectedCourse : "Выберите кружок"}
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="placeholder" className="text-2xl" disabled>
                            Выберите кружок
                        </SelectItem>
                        <SelectItem value="Робототехника" className="text-2xl">Робототехника</SelectItem>
                        <SelectItem value="Основы программирования" className="text-2xl">Основы программирования</SelectItem>
                        <SelectItem value="Разработка игр" className="text-2xl">Разработка игр</SelectItem>
                        <SelectItem value="Динамическое программирование" className="text-2xl">Динамическое программирование</SelectItem>
                        <SelectItem value="Web-разработка" className="text-2xl">Web-разработка</SelectItem>
                        <SelectItem value="Проектирование систем" className="text-2xl">Проектирование систем</SelectItem>
                    </SelectContent>
                </Select>
                </div>
              <Button type="submit" className="w-full bg-black text-3xl h-12">
                Отправить
              </Button>
            </form>
          </div>
        </div>
      </div>
    </div>
    </section>
  );
}

// Улучшенная функция форматирования телефона
function formatPhone(value: string): string {
    // Оставляем только цифры
    const digits = value.replace(/\D/g, "");
  
    // Применяем формат для номера телефона
    let formatted = "+7 ";
    if (digits.length > 1) formatted += `(${digits.slice(1, 4)}`;
    if (digits.length > 4) formatted += `) ${digits.slice(4, 7)}`;
    if (digits.length > 7) formatted += `-${digits.slice(7, 9)}`;
    if (digits.length > 9) formatted += `-${digits.slice(9, 11)}`;
  
    return formatted;
  }