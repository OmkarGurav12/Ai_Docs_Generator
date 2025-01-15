import Link from 'next/link'
import { Button } from '../ui/button'

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">Next.js App</span>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <nav className="flex items-center space-x-6">
            <Link href="/about" className="hover:text-foreground/80">
              About
            </Link>
            <Button variant="default" size="sm">
              Get Started
            </Button>
          </nav>
        </div>
      </div>
    </header>
  )
} 