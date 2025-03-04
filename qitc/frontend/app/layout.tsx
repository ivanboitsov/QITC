import type { Metadata } from "next";
import { Geist, Geist_Mono, Pixelify_Sans } from "next/font/google";
import localFont from "next/font/local"; // Импорт кастомного шрифта
import "./globals.css";

const geistPixelifySans = Pixelify_Sans({
  subsets: ['cyrillic', 'latin'],
  variable: '--font-pixelify_sans',
  weight: ['400', '500', '600', '700'],
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const monocraft = localFont({
  src: [
    {
      path: './fonts/Monocraft.ttf',
      weight: '400',
      style: 'normal',
    },
  ],
  variable: '--font-monocraft',
});

export const metadata: Metadata = {
  title: "QITC | Главная",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistPixelifySans.className} ${monocraft.className} antialiased`}>
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}
