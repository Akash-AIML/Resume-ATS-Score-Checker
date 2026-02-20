import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Navigation from '@/components/Navigation';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Resume Score Analyzer - AI Resume Improvement Tool',
    description: 'Upload your resume and get AI-powered scoring with personalized suggestions to improve your chances',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <Navigation />
                {children}
            </body>
        </html>
    );
}
