import React from 'react';
import PropTypes from 'prop-types';

const ChatMessage = ({ message, isUser }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
    <div
      className={`relative max-w-xl rounded-2xl px-4 py-2 ${
        isUser
          ? 'bg-blue-600 text-white'
          : 'bg-white text-gray-800 shadow-sm'
      }`}
    >
      {message}
      <div
        className={`absolute bottom-0 h-3 w-3 ${
          isUser
            ? 'right-0 translate-x-1/3 translate-y-1/3 transform bg-blue-600'
            : 'left-0 -translate-x-1/3 translate-y-1/3 transform bg-white'
        } rotate-45`}
      />
    </div>
  </div>
);

ChatMessage.propTypes = {
  message: PropTypes.string.isRequired,
  isUser: PropTypes.bool.isRequired
};

export default ChatMessage;