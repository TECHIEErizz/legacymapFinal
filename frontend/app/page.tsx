"use client"

import { useState } from "react"
import { Landing } from "@/components/landing"
import { UploadComponent } from "@/components/upload"
import { Dashboard } from "@/components/dashboard"

export default function Home() {
    const [view, setView] = useState<"landing" | "upload" | "dashboard">("landing")
    const [analysisData, setAnalysisData] = useState<any>(null)

    const handleStart = () => {
        setView("upload")
    }

    const handleAnalysisComplete = (data: any) => {
        setAnalysisData(data)
        setView("dashboard")
    }

    const handleReset = () => {
        setAnalysisData(null)
        setView("upload")
    }

    return (
        <main className="min-h-screen bg-background">
            {view === "landing" && (
                <Landing onStart={handleStart} />
            )}

            {view === "upload" && (
                <div className="container py-20">
                    <div className="mb-8 text-center">
                        <h1 className="text-3xl font-bold mb-2">Upload Project</h1>
                        <p className="text-muted-foreground">
                            Upload a ZIP file of your codebase to start the analysis
                        </p>
                    </div>
                    <UploadComponent onAnalysisComplete={handleAnalysisComplete} />
                </div>
            )}

            {view === "dashboard" && analysisData && (
                <div className="container py-8">
                    <Dashboard data={analysisData} onReset={handleReset} />
                </div>
            )}
        </main>
    )
}
