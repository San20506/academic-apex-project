import axios, { AxiosInstance, AxiosError } from 'axios'
import toast from 'react-hot-toast'
import type {
  SystemStatus,
  QuizRequest,
  StudyPlanRequest,
  CodeRequest,
  GenerationResponse,
  CodeGenerationResponse,
  FileListResponse,
  FileContentResponse,
  DocumentUploadResponse,
  AcademicApexError
} from '../types'

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      timeout: 60000, // 60 seconds for generation tasks
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        const message = this.extractErrorMessage(error)
        
        // Don't show toast for system status checks
        if (!error.config?.url?.includes('system-status')) {
          toast.error(message)
        }
        
        throw new AcademicApexError(
          message,
          error.response?.status,
          error.response?.data as string
        )
      }
    )
  }

  private extractErrorMessage(error: AxiosError): string {
    if (error.response?.data) {
      const data = error.response.data as any
      if (typeof data === 'string') return data
      if (data.detail) return data.detail
      if (data.message) return data.message
      if (data.error) return data.error
    }
    
    if (error.code === 'ECONNABORTED') {
      return 'Request timed out. The generation task may be taking longer than expected.'
    }
    
    if (error.code === 'ECONNREFUSED') {
      return 'Cannot connect to the Academic Apex backend. Please ensure the server is running.'
    }
    
    return error.message || 'An unexpected error occurred'
  }

  // System Status
  async getSystemStatus(): Promise<SystemStatus> {
    const response = await this.client.get<SystemStatus>('/system-status')
    return response.data
  }

  // Quiz Generation
  async generateQuiz(request: QuizRequest): Promise<GenerationResponse> {
    const response = await this.client.post<GenerationResponse>('/generate-quiz', request)
    return response.data
  }

  // Study Plan Generation
  async generateStudyPlan(request: StudyPlanRequest): Promise<GenerationResponse> {
    const response = await this.client.post<GenerationResponse>('/generate-study-plan', request)
    return response.data
  }

  // Code Generation
  async generateCode(request: CodeRequest): Promise<CodeGenerationResponse> {
    const response = await this.client.post<CodeGenerationResponse>('/generate-code', request)
    return response.data
  }

  // Document Upload
  async uploadDocument(file: File): Promise<DocumentUploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await this.client.post<DocumentUploadResponse>('/upload-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  }

  // File Management
  async listFiles(): Promise<FileListResponse> {
    const response = await this.client.get<FileListResponse>('/files')
    return response.data
  }

  async getFileContent(filename: string): Promise<FileContentResponse> {
    const response = await this.client.get<FileContentResponse>(`/files/${encodeURIComponent(filename)}`)
    return response.data
  }

  async downloadFile(filename: string): Promise<Blob> {
    const response = await this.client.get(`/files/${encodeURIComponent(filename)}/download`, {
      responseType: 'blob',
    })
    return response.data
  }

  // Health Check
  async ping(): Promise<{ message: string; version: string }> {
    const response = await this.client.get('/')
    return response.data
  }

  // Utility Methods
  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  async downloadGeneratedFile(filename: string): Promise<void> {
    try {
      const blob = await this.downloadFile(filename)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      toast.success(`Downloaded ${filename}`)
    } catch (error) {
      toast.error('Failed to download file')
      throw error
    }
  }

  // Validation helpers
  validateQuizRequest(request: Partial<QuizRequest>): string[] {
    const errors: string[] = []
    
    if (!request.subject?.trim()) {
      errors.push('Subject is required')
    }
    
    if (request.num_questions && (request.num_questions < 1 || request.num_questions > 50)) {
      errors.push('Number of questions must be between 1 and 50')
    }
    
    return errors
  }

  validateStudyPlanRequest(request: Partial<StudyPlanRequest>): string[] {
    const errors: string[] = []
    
    if (!request.subject?.trim()) {
      errors.push('Subject is required')
    }
    
    if (!request.duration?.trim()) {
      errors.push('Duration is required')
    }
    
    return errors
  }

  validateCodeRequest(request: Partial<CodeRequest>): string[] {
    const errors: string[] = []
    
    if (!request.functionality?.trim()) {
      errors.push('Functionality description is required')
    }
    
    if (request.module_name && !/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(request.module_name)) {
      errors.push('Module name must be a valid Python identifier')
    }
    
    return errors
  }

  validateFileUpload(file: File): string[] {
    const errors: string[] = []
    const maxSize = 50 * 1024 * 1024 // 50MB
    const allowedTypes = [
      'application/pdf',
      'text/plain',
      'image/jpeg',
      'image/png',
      'image/gif'
    ]
    
    if (file.size > maxSize) {
      errors.push(`File size must be less than ${this.formatFileSize(maxSize)}`)
    }
    
    if (!allowedTypes.includes(file.type)) {
      errors.push('File type not supported. Please upload PDF, text, or image files.')
    }
    
    return errors
  }
}

// Create singleton instance
const apiService = new ApiService()

export default apiService
