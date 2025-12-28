import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MVP Web App',
  description: 'Minimal MVP demonstrating end-to-end flow',
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

