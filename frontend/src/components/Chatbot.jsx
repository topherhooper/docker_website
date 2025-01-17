import React, { useState } from 'react';
import ChatMessage from './ChatMessage.jsx';
import ChatInput from './ChatInput.jsx';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I help you today?", isUser: false }
  ]);

  const handleSendMessage = (message) => {
    setMessages(prev => [...prev, { text: message, isUser: true }]);
    
    setTimeout(() => {
      setMessages(prev => [...prev, {
        text: "I'm a simple demo bot. I echo: " + message,
        isUser: false
      }]);
    }, 1000);
  };

  return (
    <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow-2xl">
      <div className="mx-auto max-w-3xl rounded-2xl bg-white shadow-lg">
        <div className="border-b border-gray-100 bg-white p-4">
          <h2 className="text-lg font-semibold text-gray-700">Chat Assistant</h2>
          <p className="text-sm text-gray-500">Online • Ready to help</p>
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
            <ChatInput onSendMessage={handleSendMessage} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;