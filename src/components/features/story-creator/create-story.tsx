"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Loader2 } from 'lucide-react'
import { StoryForm } from "./story-form"
import { DocumentTypeForm } from "./document-type-form"
import { DocumentPreview } from "./document-preview"

type Step = "story" | "document" | "preview" | "generating"

interface CreateStoryProps {
  onBack: () => void
}

export default function CreateStory({ onBack }: CreateStoryProps) {
  const [currentStep, setCurrentStep] = useState<Step>("story")
  const [formData, setFormData] = useState({
    story: {},
    documentType: "",
  })

  const steps = {
    story: {
      title: "Create Story",
      component: StoryForm,
    },
    document: {
      title: "Select Document Type",
      component: DocumentTypeForm,
    },
    preview: {
      title: "Preview & Download",
      component: DocumentPreview,
    },
    generating: {
      title: "Generating Document",
      component: GeneratingDocument,
    },
  }

  const handleStorySubmit = (data: any) => {
    setFormData(prev => ({ ...prev, story: data }))
    setCurrentStep("document")
  }

  const handleDocumentTypeSubmit = (data: any) => {
    setFormData(prev => ({ ...prev, documentType: data.format }))
    setCurrentStep("generating")
    // Simulate document generation
    setTimeout(() => {
      setCurrentStep("preview")
    }, 3000)
  }

  return (
    <div className="container mx-auto py-10 px-4">
      <Button
        variant="ghost"
        className="mb-6"
        onClick={onBack}
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Home
      </Button>

      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>{steps[currentStep].title}</CardTitle>
        </CardHeader>
        <CardContent>
          {currentStep === "story" && (
            <StoryForm onSubmit={handleStorySubmit} />
          )}
          {currentStep === "document" && (
            <DocumentTypeForm onSubmit={handleDocumentTypeSubmit} />
          )}
          {currentStep === "generating" && (
            <GeneratingDocument />
          )}
          {currentStep === "preview" && (
            <DocumentPreview formData={formData} />
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function GeneratingDocument() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
      <p className="text-lg font-medium">Generating your document...</p>
      <p className="text-sm text-muted-foreground">This may take a few moments</p>
    </div>
  )
}

