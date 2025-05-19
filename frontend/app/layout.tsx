import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import SessionWrapper from './SessionWrapper'; // Import SessionWrapper
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Portal Berita',
  description:
    'Portal Berita menggunakan teknik scraping dari sumber Kompas.com CNN Indonesia dan Antara News',
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Bungkus children dengan SessionWrapper (Client Component) */}
        <SessionWrapper>{children}</SessionWrapper>
      </body>
    </html>
  );
}
