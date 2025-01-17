#!/bin/bash

# Store the backend URL
BACKEND_URL=$(gcloud run services describe chatbot-backend --platform managed --region us-central1 --format 'value(status.url)')

# Test health endpoint
curl "${BACKEND_URL}/health"

# Test chat endpoint
curl -X POST "${BACKEND_URL}/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Docker?"}'