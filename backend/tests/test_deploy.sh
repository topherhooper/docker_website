#!/bin/bash

# Store the backend URL
BACKEND_URL=$(gcloud run services describe chatbot-backend --platform managed --region us-central1 --format 'value(status.url)')
# BACKEND_URL="https://chatbot-backend-614936797883.us-central1.run.app"

# Test health endpoint
curl "${BACKEND_URL}/health"
