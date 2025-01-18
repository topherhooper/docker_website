#!/bin/bash

# Strict mode
set -euo pipefail

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
    --allow-unauthenticated \
    --region us-central1 || exit 1
else
  echo "Creating new service via Cloud Build"
  # Create new service using Cloud Build
  gcloud builds submit --config cloudbuild.yaml || exit 1
fi