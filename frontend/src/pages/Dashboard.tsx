import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BookOpen,
  Calendar,
  Code2,
  FolderOpen,
  Settings,
  HelpCircle,
  Sparkles,
  Clock,
  TrendingUp,
  Zap,
  Shield,
  Brain
} from 'lucide-react'
import { useSystemStatus } from '../contexts/SystemStatusContext'
import apiService from '../services/api'
import type { FileInfo } from '../types'
import clsx from 'clsx'

const quickActions = [
  {
    name: 'Generate Quiz',
    href: '/quiz',
    icon: BookOpen,
    color: 'bg-blue-500',
    description: 'Create comprehensive diagnostic quizzes for any subject'
  },
  {
    name: 'Study Plan',
    href: '/study-plan',
    icon: Calendar,
    color: 'bg-green-500',
    description: 'Generate detailed, minute-by-minute study plans'
  },
  {
    name: 'Generate Code',
    href: '/code',
    icon: Code2,
    color: 'bg-purple-500',
    description: 'Create Python modules and utilities for academic tasks'
  },
  {
    name: 'My Files',
    href: '/files',
    icon: FolderOpen,
    color: 'bg-orange-500',
    description: 'View and manage all your generated content'
  }
]

const Dashboard: React.FC = () => {
  const { status, isHealthy } = useSystemStatus()
  const [recentFiles, setRecentFiles] = useState<FileInfo[]>([])
  const [statsLoading, setStatsLoading] = useState(true)

  useEffect(() => {
    loadRecentFiles()
  }, [])

  const loadRecentFiles = async () => {
    try {
      const response = await apiService.listFiles()
      if (response.success) {
        setRecentFiles(response.files.slice(0, 5)) // Show last 5 files
      }
    } catch (error) {
      console.warn('Failed to load recent files:', error)
    } finally {
      setStatsLoading(false)
    }
  }

  const getFileTypeIcon = (type: string) => {
    switch (type) {
      case 'md':
        return '📝'
      case 'py':
        return '🐍'
      case 'pdf':
        return '📄'
      default:
        return '📄'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="gradient-bg rounded-xl text-white p-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex items-center justify-center mb-4">
            <Brain className="h-12 w-12 mr-4" />
            <h1 className="text-4xl font-bold">Welcome to Academic Apex</h1>
          </div>
          <p className="text-xl text-blue-100 mb-6">
            Your AI-powered academic assistant for creating study plans, quizzes, and educational content using local models.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <div className="flex items-center bg-white/20 rounded-lg px-4 py-2">
              <Zap className="h-5 w-5 mr-2" />
              <span>Local AI</span>
            </div>
            <div className="flex items-center bg-white/20 rounded-lg px-4 py-2">
              <Shield className="h-5 w-5 mr-2" />
              <span>Privacy-First</span>
            </div>
            <div className="flex items-center bg-white/20 rounded-lg px-4 py-2">
              <BookOpen className="h-5 w-5 mr-2" />
              <span>Educational</span>
            </div>
          </div>
        </div>
      </div>

      {/* System Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className={clsx(
                'w-8 h-8 rounded-full flex items-center justify-center',
                status?.ollama_connected ? 'bg-green-100' : 'bg-red-100'
              )}>
                <Brain className={clsx(
                  'w-5 h-5',
                  status?.ollama_connected ? 'text-green-600' : 'text-red-600'
                )} />
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Ollama Status</h3>
              <p className={clsx(
                'text-sm',
                status?.ollama_connected ? 'text-green-600' : 'text-red-600'
              )}>
                {status?.ollama_connected ? 'Connected' : 'Disconnected'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {status?.models_available.length || 0} models available
              </p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className={clsx(
                'w-8 h-8 rounded-full flex items-center justify-center',
                status?.curator_running ? 'bg-green-100' : 'bg-red-100'
              )}>
                <Sparkles className={clsx(
                  'w-5 h-5',
                  status?.curator_running ? 'text-green-600' : 'text-red-600'
                )} />
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Curator Service</h3>
              <p className={clsx(
                'text-sm',
                status?.curator_running ? 'text-green-600' : 'text-red-600'
              )}>
                {status?.curator_running ? 'Running' : 'Offline'}
              </p>
              <p className="text-xs text-gray-500 mt-1">Prompt optimization</p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className={clsx(
                'w-8 h-8 rounded-full flex items-center justify-center',
                status?.obsidian_configured ? 'bg-green-100' : 'bg-yellow-100'
              )}>
                <FolderOpen className={clsx(
                  'w-5 h-5',
                  status?.obsidian_configured ? 'text-green-600' : 'text-yellow-600'
                )} />
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900">Obsidian Vault</h3>
              <p className={clsx(
                'text-sm',
                status?.obsidian_configured ? 'text-green-600' : 'text-yellow-600'
              )}>
                {status?.obsidian_configured ? 'Ready' : 'Not Set'}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {status?.obsidian_configured ? 'Notes saved automatically' : 'Configure in settings'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card p-8">
        <div className="flex items-center mb-6">
          <Zap className="h-6 w-6 text-primary-600 mr-3" />
          <h2 className="text-2xl font-bold text-gray-900">Quick Actions</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon
            
            return (
              <Link
                key={action.name}
                to={action.href}
                className="group p-6 card card-hover text-center transition-all duration-200"
              >
                <div className={clsx(
                  'w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform',
                  action.color
                )}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-primary-600">
                  {action.name}
                </h3>
                <p className="text-sm text-gray-600 leading-relaxed">
                  {action.description}
                </p>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card p-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center">
            <Clock className="h-6 w-6 text-primary-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Recent Activity</h2>
          </div>
          <Link to="/files" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            View All Files →
          </Link>
        </div>
        
        {statsLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="loading-spinner w-8 h-8"></div>
            <span className="ml-3 text-gray-500">Loading recent files...</span>
          </div>
        ) : recentFiles.length > 0 ? (
          <div className="space-y-4">
            {recentFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div className="text-2xl mr-4">
                  {getFileTypeIcon(file.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {file.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {apiService.formatFileSize(file.size)} • {apiService.formatDate(file.modified)}
                  </p>
                </div>
                <Link
                  to={`/files`}
                  className="btn btn-sm btn-outline"
                >
                  View
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FolderOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 mb-4">No recent activity. Start by generating your first educational content!</p>
            <div className="flex justify-center space-x-4">
              <Link to="/quiz" className="btn btn-primary">
                Create Quiz
              </Link>
              <Link to="/study-plan" className="btn btn-outline">
                Create Study Plan
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Issues/Warnings */}
      {status && status.issues.length > 0 && (
        <div className="card p-6 border-yellow-200 bg-yellow-50">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <HelpCircle className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-3 flex-1">
              <h3 className="text-lg font-medium text-yellow-800">
                System Issues Detected
              </h3>
              <div className="mt-2 text-sm text-yellow-700">
                <ul className="list-disc list-inside space-y-1">
                  {status.issues.slice(0, 3).map((issue, index) => (
                    <li key={index}>{issue}</li>
                  ))}
                  {status.issues.length > 3 && (
                    <li className="text-yellow-600">... and {status.issues.length - 3} more issues</li>
                  )}
                </ul>
              </div>
              <div className="mt-4">
                <Link
                  to="/settings"
                  className="btn btn-sm btn-secondary"
                >
                  Troubleshoot
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Getting Started */}
      <div className="card p-8 bg-primary-50 border-primary-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <HelpCircle className="h-8 w-8 text-primary-600" />
          </div>
          <div className="ml-4 flex-1">
            <h3 className="text-xl font-semibold text-primary-900 mb-4">
              Getting Started with Academic Apex
            </h3>
            <div className="space-y-3 text-sm text-primary-800">
              <div className="flex items-center">
                <span className="flex-shrink-0 w-6 h-6 bg-primary-200 text-primary-800 rounded-full flex items-center justify-center text-xs font-bold mr-3">1</span>
                <span>Ensure Ollama is running with your preferred model (e.g., mistral:7b)</span>
              </div>
              <div className="flex items-center">
                <span className="flex-shrink-0 w-6 h-6 bg-primary-200 text-primary-800 rounded-full flex items-center justify-center text-xs font-bold mr-3">2</span>
                <span>Start the curator service for enhanced prompt optimization (optional)</span>
              </div>
              <div className="flex items-center">
                <span className="flex-shrink-0 w-6 h-6 bg-primary-200 text-primary-800 rounded-full flex items-center justify-center text-xs font-bold mr-3">3</span>
                <span>Configure your Obsidian vault path in Settings for automatic note saving</span>
              </div>
              <div className="flex items-center">
                <span className="flex-shrink-0 w-6 h-6 bg-primary-200 text-primary-800 rounded-full flex items-center justify-center text-xs font-bold mr-3">4</span>
                <span>Choose a generation type above and start creating educational content!</span>
              </div>
            </div>
            <div className="mt-6 flex space-x-3">
              <Link to="/settings" className="btn btn-primary btn-sm">
                Configure Settings
              </Link>
              <Link to="/quiz" className="btn btn-outline btn-sm">
                Try Quiz Generator
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
