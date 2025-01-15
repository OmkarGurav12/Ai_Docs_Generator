"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus } from 'lucide-react'
import ProjectForm from "./project-form"
import DocumentTypeForm from "./document-type-form"
import DocumentPreview from "./document-preview"
import { z } from "zod"

type Step = "project" | "document" | "preview"

const projectSchema = z.object({
  title: z.string(),
  description: z.string(),
  client: z.string(),
})

type ProjectData = z.infer<typeof projectSchema>

interface FormData {
  project: ProjectData
  documentType: string
}

export default function DocumentGenerator() {
  const [currentStep, setCurrentStep] = useState<Step>("project")
  const [formData, setFormData] = useState<FormData>({
    project: {
      title: "",
      description: "",
      client: "",
    },
    documentType: "",
  })
  const [projects, setProjects] = useState<FormData[]>([])

  const steps: { [key in Step]: string } = {
    project: "Project Details",
    document: "Document Type",
    preview: "Preview & Download",
  }

  const updateFormData = (step: Step, data: ProjectData | string) => {
    setFormData((prev) => ({
      ...prev,
      [step]: data,
    }))
    const nextStep = getNextStep(step)
    if (nextStep) {
      setCurrentStep(nextStep)
    }
  }

  const getNextStep = (current: Step): Step | null => {
    const stepOrder: Step[] = ["project", "document", "preview"]
    const currentIndex = stepOrder.indexOf(current)
    return stepOrder[currentIndex + 1] || null
  }

  const getPreviousStep = (current: Step): Step | null => {
    const stepOrder: Step[] = ["project", "document", "preview"]
    const currentIndex = stepOrder.indexOf(current)
    return stepOrder[currentIndex - 1] || null
  }

  const handleNewProject = () => {
    if (projects.length > 0) {
      setProjects([...projects, formData])
    }
    setFormData({
      project: {
        title: "",
        description: "",
        client: "",
      },
      documentType: "",
    })
    setCurrentStep("project")
  }

  return (
    <div className="container mx-auto py-10">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-3xl font-bold">AI Document Generator</h1>
        <Button onClick={handleNewProject}>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      <Card className="max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Create New Document</CardTitle>
          <div className="flex justify-between items-center mt-4">
            {Object.entries(steps).map(([key, label], index) => (
              <div
                key={key}
                className={`flex items-center ${
                  index !== Object.keys(steps).length - 1
                    ? "flex-1 after:content-[''] after:h-[2px] after:flex-1 after:mx-2 after:bg-muted"
                    : ""
                }`}
              >
                <div
                  className={`rounded-full w-8 h-8 flex items-center justify-center text-sm ${
                    key === currentStep
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted"
                  }`}
                >
                  {index + 1}
                </div>
              </div>
            ))}
          </div>
        </CardHeader>
        <CardContent>
          {currentStep === "project" && (
            <ProjectForm onSubmit={(data) => updateFormData("project", data)} />
          )}
          {currentStep === "document" && (
            <DocumentTypeForm
              onSubmit={(data) => updateFormData("document", data.format)}
            />
          )}
          {currentStep === "preview" && (
            <DocumentPreview formData={formData} />
          )}
        </CardContent>
      </Card>

      {projects.length > 0 && (
        <div className="mt-8 max-w-3xl mx-auto">
          <h2 className="text-xl font-semibold mb-4">Your Projects</h2>
          <div className="space-y-4">
            {projects.map((project, index) => (
              <Card key={index}>
                <CardContent className="flex justify-between items-center p-6">
                  <div>
                    <h3 className="font-medium">{project.project.title}</h3>
                    <p className="text-sm text-muted-foreground">
                      {project.project.description}
                    </p>
                  </div>
                  <Button variant="secondary" onClick={() => console.log("Download", project)}>
                    Download Document
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

