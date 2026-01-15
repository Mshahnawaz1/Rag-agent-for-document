import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Chat from './components/Chat'
import './App.css'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [queryMode, setQueryMode] = useState('general')

  useEffect(() => {
    // Health check on mount
    const checkHealth = async () => {
      try {
        const res = await fetch(`${BASE_URL}/health`)
        if (res.ok) {
          const data = await res.json()
          addMessage('bot', `Connected to backend: ${data.service || 'RAG Engine API'}`)
        }
      } catch (error) {
        addMessage('bot', 'Warning: Unable to reach backend. Check that the FastAPI server is running.', true)
      }
    }
    checkHealth()
  }, [])

  const addMessage = (sender, text, isError = false) => {
    setMessages(prev => [...prev, { id: Date.now(), sender, text, isError }])
  }

  const handleUpload = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    addMessage('bot', `Uploading ${file.name}...`)

    try {
      const res = await fetch(`${BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || `Upload failed with status ${res.status}`)
      }

      addMessage('bot', data.message || 'Upload complete')
    } catch (error) {
      addMessage('bot', `Upload failed: ${error.message}`, true)
    }
  }

  const handleClearDB = async () => {
    if (!window.confirm('Are you sure you want to clear the vector database? This cannot be undone.')) {
      return
    }

    addMessage('bot', 'Clearing database...')

    try {
      const res = await fetch(`${BASE_URL}/clearDB`)
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || `Request failed with status ${res.status}`)
      }

      addMessage('bot', data.message || 'Database cleared')
    } catch (error) {
      addMessage('bot', `Clear DB failed: ${error.message}`, true)
    }
  }

  const handleAsk = async (query) => {
    if (!query.trim()) return

    addMessage('user', query)

    const endpoint = queryMode === 'ncert' ? '/ask-ncert' : '/ask'

    try {
      const res = await fetch(`${BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || `Request failed with status ${res.status}`)
      }

      let messageText = data.response || 'No response'
      if (Array.isArray(data.sources) && data.sources.length > 0) {
        messageText += '\n\nSources:\n' + data.sources.join('\n')
      }

      addMessage('bot', messageText)
    } catch (error) {
      addMessage('bot', `Request failed: ${error.message}`, true)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Document Assistant</h1>
      </header>
      <main className="app-main">
        <Sidebar
          onUpload={handleUpload}
          onClearDB={handleClearDB}
          queryMode={queryMode}
          onQueryModeChange={setQueryMode}
        />
        <Chat messages={messages} onAsk={handleAsk} />
      </main>
    </div>
  )
}

export default App
