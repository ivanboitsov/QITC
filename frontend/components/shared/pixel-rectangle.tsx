import React, { ReactNode } from 'react';

interface PixelRectangleProps {
  children: ReactNode;
  className?: string;
}

export default function PixelRectangle({ children, className }: PixelRectangleProps) {
  return (
    <div className={`relative w-fit h-fit ${className}`}>
      {/* Внешний прямоугольник */}
      <div className="absolute w-full h-full bg-[#03C9A1]"></div>
      {/* Внутренний прямоугольник */}
      <div className="absolute w-[calc(100%-30px)] h-[calc(100%+30px)] bg-[#03C9A1] 
      top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
      {/* Дети (текст и форма) */}
      <div className="relative z-10 p-4">
        {children}
      </div>
    </div>
  );
}