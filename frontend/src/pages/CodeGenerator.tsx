import React from 'react'
import { Code2 } from 'lucide-react'

const CodeGenerator: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Code2 className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Code Generator</h1>
      </div>
      
      <div className="card p-8 text-center">
        <Code2 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Code Generator Coming Soon</h2>
        <p className="text-gray-600 mb-6">
          Create Python modules and utilities for academic and educational tasks.
        </p>
        <p className="text-sm text-gray-500">
          This feature will be implemented in the next phase.
        </p>
      </div>
    </div>
  )
}

export default CodeGenerator
