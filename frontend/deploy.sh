#!/bin/bash

# Get backend URL
BACKEND_URL=$(gcloud run services describe chatbot-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

# Check if frontend service exists
SERVICE_EXISTS=$(gcloud run services describe chatbot-frontend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" 2>/dev/null)

if [ -n "$SERVICE_EXISTS" ]; then
  echo "Updating existing frontend service"
  docker build \
    --build-arg VITE_BACKEND_URL="${BACKEND_URL}" \
    -t gcr.io/fluted-citizen-269819/chatbot-frontend .
  docker push gcr.io/fluted-citizen-269819/chatbot-frontend
  
  gcloud run deploy chatbot-frontend \
    --image gcr.io/fluted-citizen-269819/chatbot-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
else
  echo "Creating new frontend service via Cloud Build"
  gcloud builds submit --config cloudbuild.yaml
fi