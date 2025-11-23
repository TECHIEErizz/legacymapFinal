"use client"

import { useState, useRef } from "react"
import { Upload, File, X, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface UploadComponentProps {
    onAnalysisComplete: (data: any) => void
}

export function UploadComponent({ onAnalysisComplete }: UploadComponentProps) {
    const [isDragging, setIsDragging] = useState(false)
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault()
        setIsDragging(true)
    }

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault()
        setIsDragging(false)
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault()
        setIsDragging(false)

        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            validateAndSetFile(e.dataTransfer.files[0])
        }
    }

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            validateAndSetFile(e.target.files[0])
        }
    }

    const validateAndSetFile = (selectedFile: File) => {
        setError(null)
        if (!selectedFile.name.endsWith('.zip')) {
            setError("Please upload a ZIP file")
            return
        }
        setFile(selectedFile)
    }

    const handleUpload = async () => {
        if (!file) return

        setLoading(true)
        setError(null)

        const formData = new FormData()
        formData.append("file", file)

        try {
            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"
            const response = await fetch(`${backendUrl}/upload-analyze`, {
                method: "POST",
                body: formData,
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}))
                throw new Error(errorData.detail || "Analysis failed")
            }

            const data = await response.json()
            onAnalysisComplete(data)
        } catch (err: any) {
            console.error("Upload error:", err)
            setError(err.message || "Failed to upload and analyze file")
        } finally {
            setLoading(false)
        }
    }

    const clearFile = () => {
        setFile(null)
        setError(null)
        if (fileInputRef.current) {
            fileInputRef.current.value = ""
        }
    }

    return (
        <div className="w-full max-w-xl mx-auto">
            <Card className={cn("border-2 border-dashed transition-colors",
                isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25"
            )}>
                <CardContent className="flex flex-col items-center justify-center py-10 space-y-4">
                    {!file ? (
                        <>
                            <div className="p-4 rounded-full bg-primary/10">
                                <Upload className="w-8 h-8 text-primary" />
                            </div>
                            <div className="text-center space-y-1">
                                <h3 className="text-lg font-semibold">Upload your Java codebase</h3>
                                <p className="text-sm text-muted-foreground">
                                    Drag & drop your ZIP file here, or click to browse
                                </p>
                            </div>
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".zip"
                                className="hidden"
                                onChange={handleFileSelect}
                            />
                            <Button
                                variant="outline"
                                onClick={() => fileInputRef.current?.click()}
                                onDragOver={handleDragOver}
                                onDragLeave={handleDragLeave}
                                onDrop={handleDrop}
                            >
                                Select ZIP File
                            </Button>
                        </>
                    ) : (
                        <div className="w-full space-y-4">
                            <div className="flex items-center justify-between p-3 border rounded-lg bg-background">
                                <div className="flex items-center space-x-3">
                                    <div className="p-2 rounded bg-primary/10">
                                        <File className="w-4 h-4 text-primary" />
                                    </div>
                                    <div className="space-y-0.5">
                                        <p className="text-sm font-medium">{file.name}</p>
                                        <p className="text-xs text-muted-foreground">
                                            {(file.size / 1024 / 1024).toFixed(2)} MB
                                        </p>
                                    </div>
                                </div>
                                <Button variant="ghost" size="sm" onClick={clearFile} disabled={loading}>
                                    <X className="w-4 h-4" />
                                </Button>
                            </div>

                            {error && (
                                <div className="flex items-center space-x-2 text-sm text-destructive bg-destructive/10 p-3 rounded-lg">
                                    <AlertCircle className="w-4 h-4" />
                                    <span>{error}</span>
                                </div>
                            )}

                            <Button
                                className="w-full"
                                onClick={handleUpload}
                                disabled={loading}
                            >
                                {loading ? (
                                    <div className="flex items-center space-x-2">
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                        <span>Analyzing...</span>
                                    </div>
                                ) : (
                                    "Start Analysis"
                                )}
                            </Button>
                        </div>
                    )}
                </CardContent>
            </Card>

            <div className="mt-4 text-center text-xs text-muted-foreground">
                Supported files: .zip containing .java files
            </div>
        </div>
    )
}
