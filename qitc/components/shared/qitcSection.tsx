"use client";

export default function QITCSection() {
  return (
    <section id="qiut-section">
    <div className="flex flex-col w-full h-[1120px] items-center justify-center fixed-width-container">
      {/* Центральный контейнер с тремя блоками */}
      <div className="flex w-full h-full max-w justify-between px-8 grid-background mt-20">
        <div className="flex flex-col justify-start w-1/3 text-right mt-20">
            <div
                className="bg-[#03C9A1] p-4 rounded-lg inline-block"
                style={{ 
                imageRendering: "pixelated", 
                borderRadius: "15px" /* Установите небольшой радиус */
                }}>
                <p className="text-8xl font-semibold text-white">
                1 000 000
                </p>
                <p className="text-4xl text-black">
                съеденных во время онлайн-пар печенек
                </p>
            </div>
        </div>



        {/* Центральный блок */}
        <div className="flex items-center justify-center w-1/3">
            <p
                className="font-bold text-black mt-64 animate-levitate delay-1"
                style={{ fontSize: "32rem" }}
            >
                Q
            </p>
            <p
                className="font-bold text-[#03C9A1] mt-20 animate-levitate delay-2"
                style={{ fontSize: "32rem" }}
            >
                I
            </p>
            <p
                className="font-bold text-[#03C9A1] mb-20 animate-levitate delay-3"
                style={{ fontSize: "32rem" }}
            >
                T
            </p>
            <p
                className="font-bold text-black mb-64 animate-levitate delay-4"
                style={{ fontSize: "32rem" }}
            >
                C
            </p>
        </div>

        {/* Правый блок */}
        <div className="flex flex-col justify-end w-1/3 text-left mb-20">
            <div 
                className="bg-[#03C9A1] p-4 rounded-lg inline-block"
                style={{ 
                    imageRendering: "pixelated", 
                    borderRadius: "15px" /* Установите небольшой радиус */
                    }}>
                <p className="text-8xl text-white font-semibold mb-2">
                150 000
                </p>
                <p className="text-4xl text-black">
                наших учеников не получили красный диплом после окончания школы
                </p>
            </div>
        </div>
      </div>
    </div>
    </section>
  );
}