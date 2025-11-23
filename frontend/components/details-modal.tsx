"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"

interface CallSite {
    file: string
    lines: number[]
    count: number
}

interface FunctionDetails {
    name: string
    file: string
    language: string
    called_in: CallSite[]
    dependencies: string[]
    call_count: number
}

interface DetailsModalProps {
    isOpen: boolean
    onClose: () => void
    functionDetails: FunctionDetails | null
    loading: boolean
}

export function DetailsModal({ isOpen, onClose, functionDetails, loading }: DetailsModalProps) {
    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent onClose={onClose} className="max-w-2xl max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>
                        {loading ? "Loading..." : functionDetails?.name || "Function Details"}
                    </DialogTitle>
                    <DialogDescription>
                        {!loading && functionDetails && (
                            <span className="text-sm">
                                {functionDetails.file} • {functionDetails.language}
                            </span>
                        )}
                    </DialogDescription>
                </DialogHeader>

                {loading && (
                    <div className="flex items-center justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                    </div>
                )}

                {!loading && functionDetails && (
                    <div className="space-y-6">
                        {/* Call Sites Section */}
                        <div>
                            <h3 className="text-lg font-semibold mb-3">
                                Called In ({functionDetails.call_count} times)
                            </h3>
                            {functionDetails.called_in.length === 0 ? (
                                <p className="text-sm text-muted-foreground">
                                    This function is not called anywhere in the codebase.
                                </p>
                            ) : (
                                <div className="space-y-2">
                                    {functionDetails.called_in.map((callSite, idx) => (
                                        <div
                                            key={idx}
                                            className="border rounded-lg p-3 bg-muted/50"
                                        >
                                            <div className="font-medium text-sm mb-1">
                                                {callSite.file}
                                            </div>
                                            <div className="text-xs text-muted-foreground">
                                                Lines: {callSite.lines.join(", ")} ({callSite.count} call{callSite.count !== 1 ? 's' : ''})
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Dependencies Section */}
                        <div>
                            <h3 className="text-lg font-semibold mb-3">
                                Dependencies ({functionDetails.dependencies.length})
                            </h3>
                            {functionDetails.dependencies.length === 0 ? (
                                <p className="text-sm text-muted-foreground">
                                    This function has no detected dependencies.
                                </p>
                            ) : (
                                <div className="flex flex-wrap gap-2">
                                    {functionDetails.dependencies.map((dep, idx) => (
                                        <span
                                            key={idx}
                                            className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary"
                                        >
                                            {dep}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog>
    )
}
