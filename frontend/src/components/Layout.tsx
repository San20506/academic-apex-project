import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  GraduationCap, 
  Home, 
  BookOpen, 
  Calendar, 
  Code2, 
  FolderOpen, 
  Settings,
  Menu,
  X,
  Circle,
  AlertTriangle,
  CheckCircle
} from 'lucide-react'
import { useSystemStatus } from '../contexts/SystemStatusContext'
import clsx from 'clsx'

interface LayoutProps {
  children: React.ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Generate Quiz', href: '/quiz', icon: BookOpen },
  { name: 'Study Plan', href: '/study-plan', icon: Calendar },
  { name: 'Generate Code', href: '/code', icon: Code2 },
  { name: 'File Manager', href: '/files', icon: FolderOpen },
  { name: 'Settings', href: '/settings', icon: Settings },
]

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { status, isHealthy, isLoading } = useSystemStatus()
  const location = useLocation()

  const getStatusIcon = () => {
    if (isLoading) {
      return <Circle className="w-3 h-3 text-gray-400 animate-pulse" />
    }
    
    if (isHealthy) {
      return <CheckCircle className="w-3 h-3 text-green-500" />
    }
    
    if (status?.ollama_connected || status?.curator_running) {
      return <AlertTriangle className="w-3 h-3 text-yellow-500" />
    }
    
    return <X className="w-3 h-3 text-red-500" />
  }

  const getStatusText = () => {
    if (isLoading) return 'Checking...'
    if (isHealthy) return 'All Systems Online'
    if (status?.ollama_connected || status?.curator_running) return 'Partial Service'
    return 'Service Issues'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile menu */}
      <div className={clsx(
        'fixed inset-0 flex z-40 md:hidden',
        sidebarOpen ? 'block' : 'hidden'
      )}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        
        <div className="relative flex-1 flex flex-col max-w-xs w-full pt-5 pb-4 bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-white" />
            </button>
          </div>
          
          <div className="flex-shrink-0 flex items-center px-4">
            <GraduationCap className="h-8 w-8 text-primary-600" />
            <span className="ml-2 text-xl font-semibold text-gray-900">Academic Apex</span>
          </div>
          
          <div className="mt-5 flex-1 h-0 overflow-y-auto">
            <nav className="px-2 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                const Icon = item.icon
                
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={clsx(
                      'group flex items-center px-2 py-2 text-base font-medium rounded-md transition-colors',
                      isActive 
                        ? 'bg-primary-100 text-primary-900' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    )}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon className={clsx(
                      'mr-4 flex-shrink-0 h-6 w-6',
                      isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                    )} />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Static sidebar for desktop */}
      <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div className="flex flex-col flex-grow border-r border-gray-200 pt-5 bg-white overflow-y-auto">
          <div className="flex items-center flex-shrink-0 px-4">
            <GraduationCap className="h-8 w-8 text-primary-600" />
            <span className="ml-2 text-xl font-semibold text-gray-900">Academic Apex</span>
          </div>
          
          <div className="mt-5 flex-grow flex flex-col">
            <nav className="flex-1 px-2 pb-4 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href
                const Icon = item.icon
                
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={clsx(
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors',
                      isActive 
                        ? 'bg-primary-100 text-primary-900' 
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    )}
                  >
                    <Icon className={clsx(
                      'mr-3 flex-shrink-0 h-5 w-5',
                      isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                    )} />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
            
            {/* System Status */}
            <div className="flex-shrink-0 p-4 border-t border-gray-200">
              <div className="flex items-center">
                {getStatusIcon()}
                <span className="ml-2 text-sm font-medium text-gray-700">
                  {getStatusText()}
                </span>
              </div>
              
              {status && status.issues.length > 0 && (
                <div className="mt-2">
                  <p className="text-xs text-gray-500">Issues:</p>
                  <ul className="text-xs text-red-600 mt-1">
                    {status.issues.slice(0, 2).map((issue, index) => (
                      <li key={index} className="truncate">• {issue}</li>
                    ))}
                    {status.issues.length > 2 && (
                      <li className="text-gray-500">... and {status.issues.length - 2} more</li>
                    )}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="md:pl-64 flex flex-col">
        <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
          <button
            type="button"
            className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 md:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <div className="flex-1 px-4 flex justify-between items-center">
            <div className="flex-1">
              <h1 className="text-lg font-semibold text-gray-900">
                {navigation.find(nav => nav.href === location.pathname)?.name || 'Academic Apex'}
              </h1>
            </div>
            
            <div className="ml-4 flex items-center md:ml-6">
              {/* System status indicator */}
              <div className="flex items-center space-x-2">
                {getStatusIcon()}
                <span className="hidden sm:block text-sm text-gray-500">
                  {getStatusText()}
                </span>
              </div>
            </div>
          </div>
        </div>

        <main className="flex-1">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              {children}
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 md:px-8">
            <div className="flex justify-between items-center">
              <p className="text-sm text-gray-500">
                © 2025 Academic Apex Strategist - Built with ❤️ for local-first AI education
              </p>
              <div className="flex space-x-4 text-xs text-gray-400">
                <span>🤖 Local AI</span>
                <span>🔒 Privacy-First</span>
                <span>📚 Educational</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default Layout
