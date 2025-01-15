"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { FileText, FileIcon as FilePdf } from 'lucide-react'

const documentTypeSchema = z.object({
  format: z.string().min(1, "Please select a document format"),
})

type DocumentTypeValues = z.infer<typeof documentTypeSchema>

interface DocumentTypeFormProps {
  onSubmit: (data: DocumentTypeValues) => void
}

export default function DocumentTypeForm({ onSubmit }: DocumentTypeFormProps) {
  const form = useForm<DocumentTypeValues>({
    resolver: zodResolver(documentTypeSchema),
    defaultValues: {
      format: "",
    },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="format"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Document Format</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select document format" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="word" className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Microsoft Word (.docx)
                  </SelectItem>
                  <SelectItem value="pdf" className="flex items-center gap-2">
                    <FilePdf className="h-4 w-4" />
                    PDF Document (.pdf)
                  </SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Generate Document
        </Button>
      </form>
    </Form>
  )
}

