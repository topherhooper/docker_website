import React, { useState } from 'react';
import ChatMessage from './ChatMessage.jsx';
import ChatInput from './ChatInput.jsx';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your Docker assistant. How can I help you today?", isUser: false }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message) => {
    try {
      setIsLoading(true);
      // Add user message to chat
      setMessages(prev => [...prev, { text: message, isUser: true }]);

      // Use the deployed backend URL from environment variables
      const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

      // Send message to backend
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      // Add bot response to chat
      setMessages(prev => [...prev, {
        text: data.response,
        isUser: false
      }]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message to chat
      setMessages(prev => [...prev, {
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow-2xl">
      <div className="mx-auto max-w-3xl rounded-2xl bg-white shadow-lg">
        <div className="border-b border-gray-100 bg-white p-4">
          <h2 className="text-lg font-semibold text-gray-700">Docker Assistant</h2>
          <p className="text-sm text-gray-500">
            {isLoading ? 'Thinking...' : 'Online • Ready to help'}
          </p>
        </div>
        <div className="flex h-[500px] flex-col">
          <div className="flex-1 space-y-4 overflow-y-auto bg-gray-50 p-4">
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message.text}
                isUser={message.isUser}
              />
            ))}
          </div>
          <div className="border-t border-gray-100 bg-white p-4">
            <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;