import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Impiricus Message Classifier",
    description: "Search and classify messages",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}

