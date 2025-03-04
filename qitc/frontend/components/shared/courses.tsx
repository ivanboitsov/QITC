import PixelRectangle from "./pixel-rectangle";

export default function Courses() {
  // Массив курсов с данными
  const courses = [
    { title: "Курс 1", description: "Краткое описание курса 1" },
    { title: "Курс 2", description: "Краткое описание курса 2" },
    { title: "Курс 3", description: "Краткое описание курса 3" },
    { title: "Курс 4", description: "Краткое описание курса 4" },
    { title: "Курс 5", description: "Краткое описание курса 5" },
    { title: "Курс 6", description: "Краткое описание курса 6" },
  ];

  return (
    <section id="courses">
      <div className="w-full border-t p-8 fixed-width-container">
        {/* Заголовок */}
        <div className="text-center mb-8">
          <h2 className="text-3xl">
            Познакомьте своего ребенка с востребованными на рынке навыками уже сейчас
          </h2>
        </div>

        {/* Сетка 3x2, которая занимает всё оставшееся пространство */}
        <div className="flex-1 grid grid-cols-3 gap-4">
          {courses.map((course, index) => (
            // Обертка для растягивания плитки на всю ячейку сетки и центрирования
            <div key={index} className="w-full h-full flex items-center justify-center">
              <PixelRectangle className="w-540 h-540 flex-col justify-center p-4 inline-block">
                <p className="text-2xl text-center">{course.title}</p>
                <p className="mt-2 text-sm text-center">{course.description}</p>
              </PixelRectangle>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
