import { Button } from "@/components/ui/button"
import { ArrowRight, Code, Layers, ShieldAlert, Zap } from "lucide-react"

interface LandingProps {
    onStart: () => void
}

export function Landing({ onStart }: LandingProps) {
    return (
        <div className="flex flex-col min-h-screen">
            <header className="px-4 lg:px-6 h-14 flex items-center border-b">
                <div className="flex items-center justify-center gap-2">
                    <Layers className="h-6 w-6" />
                    <span className="font-bold text-xl">LegacyMap</span>
                </div>
                <nav className="ml-auto flex gap-4 sm:gap-6">
                    <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                        Features
                    </a>
                    <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                        Documentation
                    </a>
                    <a className="text-sm font-medium hover:underline underline-offset-4" href="#">
                        GitHub
                    </a>
                </nav>
            </header>
            <main className="flex-1">
                <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
                    <div className="container px-4 md:px-6">
                        <div className="flex flex-col items-center space-y-4 text-center">
                            <div className="space-y-2">
                                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                                    Map Your Legacy Codebase
                                </h1>
                                <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                                    Visualize dependencies, identify risk areas, and understand function calls in seconds.
                                    Specialized for Java codebases.
                                </p>
                            </div>
                            <div className="space-x-4">
                                <Button size="lg" onClick={onStart}>
                                    Get Started
                                    <ArrowRight className="ml-2 h-4 w-4" />
                                </Button>
                                <Button variant="outline" size="lg">
                                    View Demo
                                </Button>
                            </div>
                        </div>
                    </div>
                </section>
                <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
                    <div className="container px-4 md:px-6">
                        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
                            <div className="flex flex-col items-center space-y-4 text-center">
                                <div className="p-4 bg-white dark:bg-gray-900 rounded-full">
                                    <Code className="h-10 w-10 text-primary" />
                                </div>
                                <h2 className="text-xl font-bold">Code Analysis</h2>
                                <p className="text-gray-500 dark:text-gray-400">
                                    Deep static analysis to extract functions, classes, and their relationships.
                                </p>
                            </div>
                            <div className="flex flex-col items-center space-y-4 text-center">
                                <div className="p-4 bg-white dark:bg-gray-900 rounded-full">
                                    <Layers className="h-10 w-10 text-primary" />
                                </div>
                                <h2 className="text-xl font-bold">Dependency Mapping</h2>
                                <p className="text-gray-500 dark:text-gray-400">
                                    Visualize how files and modules interact with each other across your project.
                                </p>
                            </div>
                            <div className="flex flex-col items-center space-y-4 text-center">
                                <div className="p-4 bg-white dark:bg-gray-900 rounded-full">
                                    <ShieldAlert className="h-10 w-10 text-primary" />
                                </div>
                                <h2 className="text-xl font-bold">Risk Assessment</h2>
                                <p className="text-gray-500 dark:text-gray-400">
                                    Identify high-risk files based on complexity and dependency coupling.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
            <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
                <p className="text-xs text-gray-500 dark:text-gray-400">
                    © 2025 LegacyMap. All rights reserved.
                </p>
                <nav className="sm:ml-auto flex gap-4 sm:gap-6">
                    <a className="text-xs hover:underline underline-offset-4" href="#">
                        Terms of Service
                    </a>
                    <a className="text-xs hover:underline underline-offset-4" href="#">
                        Privacy
                    </a>
                </nav>
            </footer>
        </div>
    )
}
