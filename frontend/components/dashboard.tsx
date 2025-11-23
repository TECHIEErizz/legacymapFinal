"use client"

import { useState } from "react"
import { Search, FileCode, Box, AlertTriangle, ArrowRight, Layers } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { MetricsCard } from "@/components/metrics-card"
import { DetailsModal } from "@/components/details-modal"
import { cn } from "@/lib/utils"
import ReactMarkdown from 'react-markdown'

interface DashboardProps {
    data: any
    onReset: () => void
}

export function Dashboard({ data, onReset }: DashboardProps) {
    const [searchTerm, setSearchTerm] = useState("")
    const [selectedFunction, setSelectedFunction] = useState<any>(null)
    const [detailsLoading, setDetailsLoading] = useState(false)
    const [detailsModalOpen, setDetailsModalOpen] = useState(false)
    const [aiSummary, setAiSummary] = useState<string | null>(null) // State for AI generated summary
    const [isGeneratingSummary, setIsGeneratingSummary] = useState(false) // State for AI summary loading

    const dataSummary = data.summary || {} // Renamed to avoid conflict with AI summary state
    const functions = data.functions || []
    const files = data.files || []

    // Filter functions based on search
    const filteredFunctions = functions.filter((func: any) =>
        func.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        func.file.toLowerCase().includes(searchTerm.toLowerCase())
    )

    const handleFunctionClick = async (func: any) => {
        setSelectedFunction(func)
        setDetailsModalOpen(true)
        setDetailsLoading(true)

        try {
            // Fetch details
            const encodedFile = encodeURIComponent(func.file)
            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/function-details/${data.repo_id}/${encodedFile}/${func.name}`)
            if (response.ok) {
                const details = await response.json()
                setSelectedFunction({ ...func, ...details })
            }
        } catch (error) {
            console.error("Error fetching details:", error)
        } finally {
            setDetailsLoading(false)
        }
    }

    const handleGenerateSummary = async () => {
        setIsGeneratingSummary(true)
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/generate-summary/${data.repo_id}`, {
                method: 'POST',
            })
            const result = await response.json()
            setAiSummary(result.summary)
        } catch (error) {
            console.error("Error generating summary:", error)
            setAiSummary("Failed to generate summary. Please try again.")
        } finally {
            setIsGeneratingSummary(false)
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
                <div className="flex gap-2">
                    <Button
                        onClick={handleGenerateSummary}
                        disabled={isGeneratingSummary}
                        variant="outline"
                    >
                        {isGeneratingSummary ? "Generating..." : "✨ AI Summary"}
                    </Button>
                    <Button onClick={onReset} variant="outline">Upload New File</Button>
                </div>
            </div>

            {aiSummary && (
                <Card className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-950/30 dark:to-purple-950/30 border-indigo-200 dark:border-indigo-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <span className="text-2xl">🤖</span> AI Executive Summary
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="prose dark:prose-invert max-w-none">
                            <ReactMarkdown>{aiSummary}</ReactMarkdown>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Metrics Overview */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <MetricsCard
                    title="Total Files"
                    value={dataSummary.total_files || 0}
                    icon={<FileCode className="h-4 w-4 text-muted-foreground" />}
                />
                <MetricsCard
                    title="Total Functions"
                    value={dataSummary.total_functions || 0}
                    icon={<Box className="h-4 w-4 text-muted-foreground" />}
                />
                <MetricsCard
                    title="Lines of Code"
                    value={dataSummary.total_loc || 0}
                    icon={<Layers className="h-4 w-4 text-muted-foreground" />}
                />
                <MetricsCard
                    title="Avg Risk Score"
                    value={dataSummary.average_risk_score || 0}
                    description="Lower is better"
                    icon={<AlertTriangle className="h-4 w-4 text-muted-foreground" />}
                />
            </div>

            {/* Main Content Area */}
            <div className="grid gap-6 md:grid-cols-7">
                {/* Function List */}
                <Card className="md:col-span-4 lg:col-span-5">
                    <CardHeader>
                        <CardTitle>Functions & Classes</CardTitle>
                        <div className="pt-4">
                            <div className="relative">
                                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                                <Input
                                    placeholder="Search functions or files..."
                                    className="pl-8"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="rounded-md border">
                            <div className="grid grid-cols-12 gap-4 p-4 border-b bg-muted/50 font-medium text-sm">
                                <div className="col-span-4">Name</div>
                                <div className="col-span-2">Type</div>
                                <div className="col-span-5">File</div>
                                <div className="col-span-1"></div>
                            </div>
                            <div className="max-h-[500px] overflow-y-auto">
                                {filteredFunctions.length === 0 ? (
                                    <div className="p-8 text-center text-muted-foreground">
                                        No functions found matching your search.
                                    </div>
                                ) : (
                                    filteredFunctions.map((func: any, i: number) => (
                                        <div
                                            key={i}
                                            className="grid grid-cols-12 gap-4 p-4 border-b last:border-0 items-center hover:bg-muted/30 transition-colors cursor-pointer"
                                            onClick={() => handleFunctionClick(func)}
                                        >
                                            <div className="col-span-4 font-medium truncate" title={func.name}>
                                                {func.name}
                                            </div>
                                            <div className="col-span-2 text-xs">
                                                <span className={cn(
                                                    "px-2 py-1 rounded-full",
                                                    func.type === 'class' ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300" : "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300"
                                                )}>
                                                    {func.type}
                                                </span>
                                            </div>
                                            <div className="col-span-5 text-sm text-muted-foreground truncate" title={func.file}>
                                                {func.file}
                                            </div>
                                            <div className="col-span-1 flex justify-end">
                                                <ArrowRight className="h-4 w-4 text-muted-foreground" />
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                        <div className="mt-4 text-xs text-muted-foreground text-center">
                            Showing {filteredFunctions.length} of {functions.length} functions
                        </div>
                    </CardContent>
                </Card>

                {/* High Risk Files */}
                <Card className="md:col-span-3 lg:col-span-2">
                    <CardHeader>
                        <CardTitle>High Risk Files</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {files
                                .sort((a: any, b: any) => b.risk_score - a.risk_score)
                                .slice(0, 5)
                                .map((file: any, i: number) => (
                                    <div key={i} className="flex flex-col space-y-1 border-b last:border-0 pb-3 last:pb-0">
                                        <div className="flex items-center justify-between">
                                            <span className="font-medium text-sm truncate max-w-[150px]" title={file.path}>
                                                {file.path.split('/').pop()}
                                            </span>
                                            <span className={cn(
                                                "text-xs font-bold px-2 py-0.5 rounded",
                                                file.risk_level === 'HIGH' ? "bg-red-100 text-red-700" :
                                                    file.risk_level === 'MEDIUM' ? "bg-yellow-100 text-yellow-700" :
                                                        "bg-green-100 text-green-700"
                                            )}>
                                                {file.risk_score}
                                            </span>
                                        </div>
                                        <div className="text-xs text-muted-foreground flex justify-between">
                                            <span>LOC: {file.loc}</span>
                                            <span>Deps: {file.imports_count}</span>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <DetailsModal
                isOpen={detailsModalOpen}
                onClose={() => setDetailsModalOpen(false)}
                functionDetails={selectedFunction}
                loading={detailsLoading}
            />
        </div>
    )
}
