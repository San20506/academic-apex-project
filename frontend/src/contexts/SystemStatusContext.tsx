import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import apiService from '../services/api'
import type { SystemStatus } from '../types'

interface SystemStatusContextType {
  status: SystemStatus | null
  isLoading: boolean
  error: string | null
  refreshStatus: () => Promise<void>
  isHealthy: boolean
}

const SystemStatusContext = createContext<SystemStatusContextType | undefined>(undefined)

export const useSystemStatus = () => {
  const context = useContext(SystemStatusContext)
  if (context === undefined) {
    throw new Error('useSystemStatus must be used within a SystemStatusProvider')
  }
  return context
}

interface SystemStatusProviderProps {
  children: ReactNode
}

export const SystemStatusProvider: React.FC<SystemStatusProviderProps> = ({ children }) => {
  const [status, setStatus] = useState<SystemStatus | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshStatus = async () => {
    try {
      setError(null)
      const newStatus = await apiService.getSystemStatus()
      setStatus(newStatus)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch system status')
      console.warn('System status check failed:', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Calculate if system is healthy
  const isHealthy = status ? 
    status.ollama_connected && status.curator_running && status.issues.length === 0 : 
    false

  useEffect(() => {
    // Initial status check
    refreshStatus()

    // Set up periodic status checks every 30 seconds
    const interval = setInterval(refreshStatus, 30000)

    return () => clearInterval(interval)
  }, [])

  const value: SystemStatusContextType = {
    status,
    isLoading,
    error,
    refreshStatus,
    isHealthy
  }

  return (
    <SystemStatusContext.Provider value={value}>
      {children}
    </SystemStatusContext.Provider>
  )
}

export default SystemStatusContext
