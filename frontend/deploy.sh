#!/bin/bash

# Strict mode
set -euo pipefail

# Ensure we're logged in
if ! gcloud auth print-access-token >/dev/null 2>&1; then
    echo "Not logged in to gcloud. Run 'gcloud auth login' first"
    exit 1
fi

# Get backend URL
BACKEND_URL=$(gcloud run services describe chatbot-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)') || {
    echo "Failed to get backend URL. Is backend service running?"
    exit 1
}

# Check if frontend service exists
SERVICE_EXISTS=$(gcloud run services describe chatbot-frontend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" 2>/dev/null || true)

if [ -n "$SERVICE_EXISTS" ]; then
  echo "Updating existing frontend service"
  # Configure docker auth
  gcloud auth configure-docker --quiet || exit 1
  
  docker build \
    --build-arg VITE_BACKEND_URL="${BACKEND_URL}" \
    -t gcr.io/fluted-citizen-269819/chatbot-frontend . || exit 1
    
  docker push gcr.io/fluted-citizen-269819/chatbot-frontend || exit 1
  
  gcloud run deploy chatbot-frontend \
    --image gcr.io/fluted-citizen-269819/chatbot-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated || exit 1
else
  echo "Creating new frontend service via Cloud Build"
  gcloud builds submit --config cloudbuild.yaml || exit 1
fi