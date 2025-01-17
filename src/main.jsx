import React from 'react';
import ReactDOM from 'react-dom/client';
import { Chatbot } from './components';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
      <Chatbot />
    </div>
  </React.StrictMode>
);