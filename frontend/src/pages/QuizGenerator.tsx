import React from 'react'
import { BookOpen } from 'lucide-react'

const QuizGenerator: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <BookOpen className="h-8 w-8 text-primary-600 mr-3" />
        <h1 className="text-3xl font-bold text-gray-900">Quiz Generator</h1>
      </div>
      
      <div className="card p-8 text-center">
        <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Quiz Generator Coming Soon</h2>
        <p className="text-gray-600 mb-6">
          Create comprehensive diagnostic quizzes for any subject with customizable difficulty levels.
        </p>
        <p className="text-sm text-gray-500">
          This feature will be implemented in the next phase.
        </p>
      </div>
    </div>
  )
}

export default QuizGenerator
