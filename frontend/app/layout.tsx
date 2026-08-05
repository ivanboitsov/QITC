import "./globals.css";
import type { Metadata } from "next";
import localFont from "next/font/local";
import { Pixelify_Sans } from "next/font/google";

const geistPixelifySans = Pixelify_Sans({
  subsets: ['cyrillic', 'latin'],
  variable: '--font-pixelify_sans',
  weight: ['400', '500', '600', '700'],
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
