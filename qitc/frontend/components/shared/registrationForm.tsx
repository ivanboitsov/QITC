"use client";
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import { Label } from "@/components/ui/label";

import PixelRectangle from "./pixel-rectangle";

export default function RegistrationForm() {
    const [selectedCourse, setSelectedCourse] = React.useState("placeholder");

  return (
    <section id="registration-form">
    {/* Верхняя надпись */}
    <h1 className="text-3xl text-center px-4 mb-8">
      Место, где начинается великая история будущих лидеров технологий
    </h1>
    <div className="flex w-full h-[900px] items-center justify-center border-t fixed-width-container">
      <div className="flex w-full h-full items-center max-w justify-between px-52 grid-background">
        <PixelRectangle>
        <div className="flex flex-col md:flex-row gap-6 p-12">
          <div className="flex-1 text-4xl text-white">
            <p>
              Если у вас появилось желание записаться в кружок или остались вопросы — заполните заявку, и мы обязательно с вами свяжемся.
            </p>
          </div>
          <div className="flex-1">
            <form className="space-y-6">
              <div>
                <Label htmlFor="fio" className="text-2xl">Имя</Label>
                <Input 
                    id="fio" 
                    name="fio" 
                    className="text-xl w-full h-14 px-4" 
                    placeholder="Введите ваше имя" 
                    style={{fontSize: "1.875rem"}}
                />
              </div>
              <div>
                <Label htmlFor="phone" className="text-2xl">Телефон</Label>
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
                <Label htmlFor="email" className="text-2xl">Почта</Label>
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
                <Label htmlFor="course" className="text-2xl">Кружок</Label>
                <Select
                    onValueChange={(value) => setSelectedCourse(value)}
                    value={selectedCourse}>
                    <SelectTrigger id="course" className="text-xl h-14" style={{fontSize: "1.875rem"}}>
                    {selectedCourse !== "placeholder" ? selectedCourse : "Выберите кружок"}
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="placeholder" className="text-xl" disabled>
                            Выберите кружок
                        </SelectItem>
                        <SelectItem value="Робототехника" className="text-xl">Робототехника</SelectItem>
                        <SelectItem value="Основы программирования" className="text-xl">Основы программирования</SelectItem>
                        <SelectItem value="Разработка игр" className="text-xl">Разработка игр</SelectItem>
                        <SelectItem value="Динамическое программирование" className="text-xl">Динамическое программирование</SelectItem>
                        <SelectItem value="Web-разработка" className="text-xl">Web-разработка</SelectItem>
                        <SelectItem value="Проектирование систем" className="text-xl">Проектирование систем</SelectItem>
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