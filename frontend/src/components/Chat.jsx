import { useState, useRef, useEffect } from 'react'
import Message from './Message'

function Chat({ messages, onAsk }) {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatWindowRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight
    }
  }, [messages])

  useEffect(() => {
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 160) + 'px'
    }
  }, [query])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim() || isLoading) return

    setIsLoading(true)
    try {
      await onAsk(query)
      setQuery('')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <section className="chat-section">
      <div ref={chatWindowRef} className="chat-window">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <p>Start a conversation by asking a question about your documents.</p>
          </div>
        ) : (
          messages.map((msg) => (
            <Message key={msg.id} sender={msg.sender} text={msg.text} isError={msg.isError} />
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-container">
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your documents..."
          rows="1"
          disabled={isLoading}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className="btn btn-primary btn-send"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </section>
  )
}

export default Chat
