"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Download, FileText } from 'lucide-react'

interface DocumentPreviewProps {
  formData: {
    project: {
      title: string
      description: string
      client: string
    }
    documentType: string
  }
}

export default function DocumentPreview({ formData }: DocumentPreviewProps) {
  const handleDownload = () => {
    // TODO: Implement document download
    console.log("Downloading document:", formData)
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-4 mb-4">
            <FileText className="h-8 w-8 text-primary" />
            <div>
              <h3 className="font-medium">{formData.project.title}</h3>
              <p className="text-sm text-muted-foreground">
                {formData.documentType === "word" ? "Microsoft Word" : "PDF"} Document
              </p>
            </div>
          </div>
          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Client:</span> {formData.project.client}
            </p>
            <p className="text-sm text-muted-foreground">
              <span className="font-medium">Description:</span> {formData.project.description}
            </p>
          </div>
        </CardContent>
      </Card>

      <Button onClick={handleDownload} className="w-full">
        <Download className="mr-2 h-4 w-4" />
        Download Document
      </Button>
    </div>
  )
}
