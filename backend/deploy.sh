#!/bin/bash

# Strict mode
set -euo pipefail

# Read API key
API_KEY=$(grep OPENAI_API_KEY ../.credentials/openai.env | cut -d '=' -f2) || {
    echo "Failed to read API key from ../.credentials/openai.env"
    exit 1
}

# Check if API key is empty
if [ -z "$API_KEY" ]; then
    echo "API key is empty"
    exit 1
fi

# Check if service exists
SERVICE_EXISTS=$(gcloud run services describe chatbot-backend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" 2>/dev/null || true)

if [ -n "$SERVICE_EXISTS" ]; then
  echo "Updating existing backend service"
  # Configure docker auth
  gcloud auth configure-docker --quiet || exit 1
  
  docker build \
    -t gcr.io/fluted-citizen-269819/chatbot-backend . || exit 1
    
  docker push gcr.io/fluted-citizen-269819/chatbot-backend || exit 1
  
  # Update existing service
  gcloud run deploy chatbot-backend \
    --image gcr.io/fluted-citizen-269819/chatbot-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="OPENAI_API_KEY=${API_KEY}" || exit 1
else
  echo "Creating new service via Cloud Build"
  # Create new service using Cloud Build
  gcloud builds submit --config cloudbuild.yaml \
    --substitutions=_OPENAI_API_KEY="${API_KEY}" || exit 1
fi