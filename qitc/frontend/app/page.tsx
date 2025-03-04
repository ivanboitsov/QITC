import Header from "@/components/shared/header";
import Footer from "@/components/shared/footer";
import Courses from "@/components/shared/courses";
import QITCSection from "@/components/shared/qitcSection";
import RegistrationForm from "@/components/shared/registrationForm";


export default function Home() {
  return (
    <main className="flex flex-col min-h-screen">
      <Header />
      <div className="flex-1 p-6">
        {/* Основное содержимое страницы */}
        <QITCSection />
        <Courses />
        <RegistrationForm />
      </div>
      <Footer />
    </main>
  );
}