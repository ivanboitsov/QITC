import Header from "@/components/shared/header";
import Footer from "@/components/shared/footer";
import Courses from "@/components/shared/courses";
import QITCSection from "@/components/shared/qitcSection";
import ApplicationFrom from "@/components/shared/applicationForm";

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-1 p-6 fixed-width-container">
        {/* Основное содержимое страницы */}
        <QITCSection />
        <Courses />
        <ApplicationFrom />
      </div>
      <Footer />
    </main>
  );
}