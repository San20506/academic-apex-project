// System Status Types
export interface SystemStatus {
  ollama_connected: boolean
  curator_running: boolean
  obsidian_configured: boolean
  models_available: string[]
  issues: string[]
  last_check: string
}

// Generation Request Types
export interface QuizRequest {
  subject: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  num_questions: number
  use_curation: boolean
}

export interface StudyPlanRequest {
  subject: string
  duration: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  objectives: string[]
  use_curation: boolean
}

export interface CodeRequest {
  module_name: string
  functionality: string
  include_tests: boolean
  use_curation: boolean
}

// Generation Response Types
export interface GenerationStats {
  length: number
  model: string
  tokens: number
}

export interface GenerationResponse {
  success: boolean
  content: string
  filename: string
  obsidian_saved: boolean
  stats: GenerationStats
  error?: string
}

export interface CodeGenerationResponse extends GenerationResponse {
  syntax_valid: boolean
  syntax_error?: string
}

// File Types
export interface FileInfo {
  name: string
  size: number
  modified: string
  type: string
}

export interface FileListResponse {
  success: boolean
  files: FileInfo[]
  total: number
}

export interface FileContentResponse {
  success: boolean
  filename: string
  content: string
  size: number
}

// Document Upload Types
export interface DocumentUploadResponse {
  success: boolean
  filename: string
  extracted_text: string
  confidence: number
  processing_time: number
  file_size: number
  error?: string
}

// UI State Types
export interface LoadingState {
  isLoading: boolean
  message?: string
}

export interface FormErrors {
  [key: string]: string | undefined
}

// Theme Types
export type Theme = 'light' | 'dark' | 'auto'

// Navigation Types
export interface NavItem {
  label: string
  path: string
  icon: string
  description?: string
}

// Settings Types
export interface AppSettings {
  theme: Theme
  obsidian_vault_path: string
  default_model: string
  auto_save_obsidian: boolean
  use_curation_by_default: boolean
}

// Error Types
export interface ApiError {
  message: string
  details?: string
  status?: number
}

export class AcademicApexError extends Error {
  public status?: number
  public details?: string

  constructor(message: string, status?: number, details?: string) {
    super(message)
    this.name = 'AcademicApexError'
    this.status = status
    this.details = details
  }
}

// Utility Types
export type APIResponse<T> = {
  success: true
  data: T
} | {
  success: false
  error: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  has_next: boolean
  has_prev: boolean
}

// Component Props Types
export interface BaseComponentProps {
  className?: string
  children?: React.ReactNode
}

export interface PageProps extends BaseComponentProps {
  title?: string
}
