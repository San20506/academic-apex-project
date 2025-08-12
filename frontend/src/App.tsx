import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

// Components
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import QuizGenerator from './pages/QuizGenerator'
import StudyPlanGenerator from './pages/StudyPlanGenerator'
import CodeGenerator from './pages/CodeGenerator'
import FileManager from './pages/FileManager'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'

// Context
import { SystemStatusProvider } from './contexts/SystemStatusContext'

function App() {
  return (
    <SystemStatusProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/quiz" element={<QuizGenerator />} />
            <Route path="/study-plan" element={<StudyPlanGenerator />} />
            <Route path="/code" element={<CodeGenerator />} />
            <Route path="/files" element={<FileManager />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#374151',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </Router>
    </SystemStatusProvider>
  )
}

export default App
