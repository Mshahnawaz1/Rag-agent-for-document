function Message({ sender, text, isError }) {
  const isUser = sender === 'user'
  const isBot = sender === 'bot'

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-bot'}`}>
      <div className={`message-bubble ${isError ? 'message-error' : ''}`}>
        <p className="message-text">{text}</p>
      </div>
    </div>
  )
}

export default Message
