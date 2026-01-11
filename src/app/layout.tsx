import type { Metadata } from "next";
import { Playfair_Display, Lato } from "next/font/google";
import "./globals.css";
import { LanguageProvider } from "@/context/LanguageContext";
import Banner from "@/components/Banner";
import ThemeDecorations from "@/components/ThemeDecorations";

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-serif",
  display: "swap",
});

const lato = Lato({
  weight: ["400", "700"],
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "ink dynasty",
  description: "nnnwwb`s portfollio",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="lv" className={`${playfair.variable} ${lato.variable}`}>
      <body>
        <LanguageProvider>
          <Banner />
          <ThemeDecorations />
          {children}
        </LanguageProvider>
      </body>
    </html>
  );
}
