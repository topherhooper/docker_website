#!/bin/bash

# Read API key
API_KEY=$(grep OPENAI_API_KEY ../.credentials/openai.env | cut -d '=' -f2)

# Check if service exists
SERVICE_EXISTS=$(gcloud run services describe chatbot-backend \
  --platform managed \
  --region us-central1 \
  --format="value(status.url)" 2>/dev/null)

if [ -n "$SERVICE_EXISTS" ]; then
  echo "Updating existing service: chatbot-backend"
  # Update existing service
  gcloud run deploy chatbot-backend \
    --image gcr.io/fluted-citizen-269819/chatbot-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="OPENAI_API_KEY=${API_KEY}"
else
  echo "Creating new service via Cloud Build"
  # Create new service using Cloud Build
  gcloud builds submit --config cloudbuild.yaml \
    --substitutions=_OPENAI_API_KEY="${API_KEY}"
fi