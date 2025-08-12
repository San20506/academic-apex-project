import React from 'react'
import { FolderOpen } from 'lucide-react'

const FileManager: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <FolderOpen className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">File Manager</h1>
      </div>
      
      <div className="card p-8 text-center">
        <FolderOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">File Manager Coming Soon</h2>
        <p className="text-gray-600 mb-6">
          View, download, and manage all your generated educational content.
        </p>
        <p className="text-sm text-gray-500">
          This feature will be implemented in the next phase.
        </p>
      </div>
    </div>
  )
}

export default FileManager
