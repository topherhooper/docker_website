// File: llm-chat/frontend/src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import ChatInterface from './components/ChatInterface.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ChatInterface />
  </React.StrictMode>,
)