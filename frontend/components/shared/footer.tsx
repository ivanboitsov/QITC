export default function Footer() {
    return (
        <footer className="w-full flex flex-col items-center justify-center p-4 border-t bg-neutral-600 text-white">
            <div className="w-[1800px] max-w-7xl flex justify-between">
                
                {/* Логотип и описание */}
                <div>
                    <div className="text-5xl font-bold tracking-wide uppercase">QITC</div>
                    <div className="text-xl">Лучший проводник в мир IT для твоего ребенка</div>
                </div>

                {/* Контакты */}
                <div className="text-xl">
                    <p>Контакты: ivanboitsov@gmail.com</p>
                    <p>Телефон: +7 (123) 456-78-90</p>
                    <p>Telegram: @e1</p>
                </div>
            </div>
        </footer>
      
    );
  }