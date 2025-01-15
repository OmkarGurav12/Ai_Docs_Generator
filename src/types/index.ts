export type BaseProps = {
  className?: string
  children?: React.ReactNode
}

export type ApiResponse<T> = {
  data: T
  error?: string
  status: number
} 