"use client";

import { Button } from "../ui/button";
import { UserRound  } from 'lucide-react';
import PixelRectangleIcon from "./pixel-rectangle-icon";

export default function Header() {

  const scrollToAnchore = (targetId: string) => {
    const element = document.getElementById(targetId);
    if (element) {
      const headerOffset = 80; // Высота хедера в пикселях
      const elementPosition = element.getBoundingClientRect().top + window.scrollY;
      const offsetPosition = elementPosition - headerOffset;
  
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    }
  };  

  return (
    <header className="w-full flex items-center justify-between p-4 border-b bg-white fixed top-0 left-0 z-50">
      {/* Логотип и ссылки */}
      <div className="flex items-center space-x-8">
        {/* Логотип */}
        <div className="text-6xl font-bold tracking-wide uppercase">QITC</div>

        {/* Ссылки для навигации */}
        <div className="flex space-x-6">
          <Button
            variant="link"
            onClick={() => scrollToAnchore("qiut-section")}
            className="text-3xl"
          >
            Главная
          </Button>
          <Button
            variant="link"
            onClick={() => scrollToAnchore("courses")}
            className="text-3xl"
          >
            Кружки
          </Button>
          <Button
            variant="link"
            onClick={() => scrollToAnchore("registration-form")}
            className="text-3xl"
          >
            Связаться с нами
          </Button>
        </div>
      </div>

      {/* Кнопка пользователя */}
      <Button
        variant="default"
        className="w-16 h-16 bg-[#03C9A1] flex items-center justify-center rounded-2xl">
          <UserRound className="text-white" />
      </Button>
      
    </header>
  );
}