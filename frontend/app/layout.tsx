import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: 'LegacyMap - Code Analysis Tool',
    description: 'Analyze legacy codebases, map dependencies, and identify risk areas',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}
