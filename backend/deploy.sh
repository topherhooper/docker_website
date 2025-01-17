#!/bin/bash

# Read API key
API_KEY=$(grep OPENAI_API_KEY ../.credentials/openai.env | cut -d '=' -f2)

# Initialize gcloud if needed
gcloud init --configuration=chatbot-deploy
gcloud config set project fluted-citizen-269819
gcloud config set run/region us-central1

# Build and deploy
gcloud builds submit --config cloudbuild.yaml

# Update environment variables
gcloud run deploy chatbot-backend \
  --image gcr.io/fluted-citizen-269819/chatbot-backend \
  --set-env-vars "OPENAI_API_KEY=${API_KEY}"