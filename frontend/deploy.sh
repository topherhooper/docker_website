#!/bin/bash
set -euo pipefail

# Check if service exists
SERVICE_EXISTS=$(gcloud run services describe chatbot-frontend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" 2>/dev/null || true)

if [ -n "$SERVICE_EXISTS" ]; then
  echo "Updating existing frontend service"
  gcloud auth configure-docker --quiet || exit 1
  
  # Get latest version of the secret
  gcloud secrets versions access latest \
    --secret=frontend-google-oauth-credentials \
    --project=fluted-citizen-269819 > oauth_credentials.json

  # Build with local secret file
  docker build \
    --secret id=google_oauth,src=oauth_credentials.json \
    -t gcr.io/fluted-citizen-269819/chatbot-frontend . || exit 1
    
  # Clean up
  rm oauth_credentials.json
    
  docker push gcr.io/fluted-citizen-269819/chatbot-frontend || exit 1
  
  gcloud run deploy chatbot-frontend \
    --image gcr.io/fluted-citizen-269819/chatbot-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated 
else
  echo "Creating new frontend service via Cloud Build"
  gcloud builds submit --config cloudbuild.yaml || exit 1
fi