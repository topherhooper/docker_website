import React, { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import PropTypes from 'prop-types';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
const Auth = ({ onSuccess }) => {
  const [error, setError] = useState(null);

  const handleError = () => {
    setError('Authentication failed. Please try again.');
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const response = await fetch(`${BACKEND_URL}/verify_token`, {
        method: 'POST',  // Must use POST to match backend endpoint
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${credentialResponse.credential}`
        }
      });

      if (!response.ok) {
        throw new Error('Token verification failed');
      }

      onSuccess(credentialResponse);
    } catch (err) {
      console.error('Authentication error:', err);
      handleError();
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100">
      <div className="mb-8 text-center">
        <h1 className="mb-2 text-3xl font-bold text-gray-800">Welcome to Chatbot</h1>
        <p className="text-gray-600">Please sign in to continue</p>
        {error && <p className="mt-2 text-red-600">{error}</p>}
      </div>
      <div className="rounded-lg bg-white p-8 shadow-lg">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={handleError}
          useOneTap
        />
      </div>
    </div>
  );
};

Auth.propTypes = {
  onSuccess: PropTypes.func.isRequired
};

export default Auth;