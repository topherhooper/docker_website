import React, { useState } from 'react';
import ChatMessage from './ChatMessage.jsx';
import ChatInput from './ChatInput.jsx';
import Auth from './Auth.jsx';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hey yung fella. What do you want?", isUser: false }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userToken, setUserToken] = useState(null);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleAuthSuccess = async (credentialResponse) => {
    try {
      const response = await fetch(`${BACKEND_URL}/verify_token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${credentialResponse.credential}`
        }
      });

      if (response.ok) {
        setUserToken(credentialResponse.credential);
        setIsAuthenticated(true);
      } else {
        console.error('Token validation failed');
      }
    } catch (error) {
      console.error('Auth error:', error);
    }
  };

  const handleSendMessage = async (message) => {
    try {
      setIsLoading(true);
      setMessages(prev => [...prev, { text: message, isUser: true }]);

      const conversation = messages.map(msg => ({
        role: msg.isUser ? "user" : "assistant",
        content: msg.text
      }));

      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${userToken}`,
        },
        body: JSON.stringify({ 
          message,
          conversation: conversation 
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, {
        text: data.response,
        isUser: false
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        text: "Sorry, I encountered an error. Please try again.",
        isUser: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <Auth onSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow-2xl">
      <div className="mx-auto max-w-3xl rounded-2xl bg-white shadow-lg">
        <div className="border-b border-gray-100 bg-white p-4">
          <h2 className="text-lg font-semibold text-gray-700">Old Man Hooper</h2>
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