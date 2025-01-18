import React from 'react';
import ReactDOM from 'react-dom/client';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Chatbot } from './components';
import './index.css';

// Import credentials directly from the JSON file
import credentials from '../.credentials/frontend_google_oath.json';
const GOOGLE_CLIENT_ID = credentials.web.client_id;

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <div className="flex min-h-screen items-center justify-center bg-gray-100 p-4">
        <Chatbot />
      </div>
    </GoogleOAuthProvider>
  </React.StrictMode>
);