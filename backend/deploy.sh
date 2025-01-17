#!/bin/bash

# Read API key
API_KEY=$(grep OPENAI_API_KEY ../.credentials/openai.env | cut -d '=' -f2)

# Build and deploy with API key substitution
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_OPENAI_API_KEY="${API_KEY}"