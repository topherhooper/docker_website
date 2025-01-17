import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Send } from 'lucide-react';

const ChatInput = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-2">
      <div className="flex-1">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          className="w-full rounded-xl bg-gray-50 px-4 py-3 text-gray-700 placeholder-gray-400 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        type="submit"
        className="rounded-xl bg-blue-600 p-3 text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        <Send size={20} />
      </button>
    </form>
  );
};

ChatInput.propTypes = {
  onSendMessage: PropTypes.func.isRequired
};

export default ChatInput;